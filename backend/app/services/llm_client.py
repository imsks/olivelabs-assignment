"""
LLM Client for OpenAI API integration
Handles prompt construction and API calls for NLQ to SQL conversion
"""

import json
from typing import Dict, List, Any, Optional
from openai import OpenAI
from app.core.config import settings
from app.services.schema_registry import schema_registry

class LLMClient:
    """Client for OpenAI API integration"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
    
    def generate_sql(self, prompt: str, conversation_context: Optional[str] = None) -> Dict[str, Any]:
        """Generate SQL from natural language prompt"""
        
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(prompt, conversation_context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            return self._parse_response(content)
            
        except Exception as e:
            raise Exception(f"LLM API error: {str(e)}")
    
    def _build_system_prompt(self) -> str:
        """Build system prompt with schema context"""
        schema_context = schema_registry.serialize_for_llm()
        
        return f"""You are a SQL expert that converts natural language queries to SQL.

Database Schema:
{schema_context}

Rules:
1. Only use SELECT statements
2. Always include proper JOINs when accessing related tables
3. Use proper column names from the schema
4. Include LIMIT clause for large result sets (max 1000 rows)
5. Use proper date formatting for date filters
6. Calculate revenue as quantity * unit_price
7. Return valid SQL only, no explanations

Examples:
- "revenue by region" -> SELECT region, SUM(quantity * unit_price) as revenue FROM orders GROUP BY region
- "orders in Q2 2024" -> SELECT * FROM orders WHERE order_date >= '2024-04-01' AND order_date < '2024-07-01'
- "top customers by revenue" -> SELECT c.name, SUM(o.quantity * o.unit_price) as revenue FROM orders o JOIN customers c ON o.customer_id = c.customer_id GROUP BY c.customer_id, c.name ORDER BY revenue DESC LIMIT 10

Return your response as JSON with this structure:
{{
    "sql": "SELECT ...",
    "explain": {{
        "filters": ["list of filter conditions"],
        "groupBy": ["list of group by columns"],
        "aggregates": ["list of aggregate functions"],
        "sourceTables": ["list of tables used"]
    }}
}}"""
    
    def _build_user_prompt(self, prompt: str, conversation_context: Optional[str] = None) -> str:
        """Build user prompt with conversation context"""
        if conversation_context:
            return f"""Previous context: {conversation_context}

Current query: {prompt}

Generate SQL for the current query, considering the previous context."""
        else:
            return f"Generate SQL for: {prompt}"
    
    def _parse_response(self, content: str) -> Dict[str, Any]:
        """Parse LLM response"""
        try:
            # Try to extract JSON from response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Fallback: treat entire content as SQL
                return {
                    "sql": content.strip(),
                    "explain": {
                        "filters": [],
                        "groupBy": [],
                        "aggregates": [],
                        "sourceTables": ["orders"]
                    }
                }
        except json.JSONDecodeError:
            # Fallback: treat entire content as SQL
            return {
                "sql": content.strip(),
                "explain": {
                    "filters": [],
                    "groupBy": [],
                    "aggregates": [],
                    "sourceTables": ["orders"]
                }
            }

# Global LLM client instance
llm_client = LLMClient()
