"""
Conversation Manager Service
Handles conversation state and context for follow-up queries
"""

import redis
import json
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from app.core.config import settings
from app.core.exceptions import ConversationNotFoundError

class ConversationManager:
    """Manages conversation state and context"""
    
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
        self.conversation_ttl = 3600  # 1 hour
        self.max_turns = 10  # Maximum turns per conversation
    
    def create_conversation(self, user_id: int) -> str:
        """Create a new conversation"""
        conversation_id = str(uuid.uuid4())
        
        conversation_data = {
            "id": conversation_id,
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "turns": [],
            "context": {
                "last_query": None,
                "last_sql": None,
                "last_explain": None
            }
        }
        
        self._save_conversation(conversation_id, conversation_data)
        return conversation_id
    
    def get_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """Get conversation by ID"""
        conversation_data = self._get_conversation(conversation_id)
        if not conversation_data:
            raise ConversationNotFoundError(f"Conversation {conversation_id} not found")
        
        return conversation_data
    
    def add_turn(self, conversation_id: str, prompt: str, sql: str, explain: Dict[str, Any]) -> None:
        """Add a turn to the conversation"""
        conversation_data = self.get_conversation(conversation_id)
        
        turn = {
            "turn_number": len(conversation_data["turns"]) + 1,
            "prompt": prompt,
            "sql": sql,
            "explain": explain,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        conversation_data["turns"].append(turn)
        
        # Update context
        conversation_data["context"]["last_query"] = prompt
        conversation_data["context"]["last_sql"] = sql
        conversation_data["context"]["last_explain"] = explain
        
        # Limit number of turns
        if len(conversation_data["turns"]) > self.max_turns:
            conversation_data["turns"] = conversation_data["turns"][-self.max_turns:]
        
        self._save_conversation(conversation_id, conversation_data)
    
    def get_context_for_followup(self, conversation_id: str) -> Optional[str]:
        """Get context string for follow-up queries"""
        conversation_data = self.get_conversation(conversation_id)
        
        if not conversation_data["turns"]:
            return None
        
        # Build context from recent turns
        context_parts = []
        
        # Include last 3 turns for context
        recent_turns = conversation_data["turns"][-3:]
        
        for turn in recent_turns:
            context_parts.append(f"Query: {turn['prompt']}")
            context_parts.append(f"SQL: {turn['sql']}")
        
        return "\n".join(context_parts)
    
    def refine_query(self, conversation_id: str, followup: str) -> Dict[str, Any]:
        """Handle follow-up query refinement"""
        conversation_data = self.get_conversation(conversation_id)
        
        if not conversation_data["turns"]:
            raise ConversationNotFoundError("No previous query to refine")
        
        # Get the last query context
        last_turn = conversation_data["turns"][-1]
        last_sql = last_turn["sql"]
        last_explain = last_turn["explain"]
        
        # Build refinement context
        refinement_context = {
            "original_query": last_turn["prompt"],
            "original_sql": last_sql,
            "original_explain": last_explain,
            "followup": followup
        }
        
        return refinement_context
    
    def _save_conversation(self, conversation_id: str, conversation_data: Dict[str, Any]) -> None:
        """Save conversation to Redis"""
        try:
            self.redis_client.setex(
                f"conversation:{conversation_id}",
                self.conversation_ttl,
                json.dumps(conversation_data)
            )
        except Exception as e:
            print(f"Failed to save conversation: {e}")
    
    def _get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get conversation from Redis"""
        try:
            cached = self.redis_client.get(f"conversation:{conversation_id}")
            if cached:
                return json.loads(cached)
        except Exception as e:
            print(f"Failed to get conversation: {e}")
        return None
    
    def cleanup_expired_conversations(self) -> None:
        """Clean up expired conversations (called periodically)"""
        # Redis TTL handles this automatically
        pass

# Global conversation manager instance
conversation_manager = ConversationManager()
