"""
Main NLQ Parser Service
Orchestrates the NLQ to SQL conversion process
"""

from typing import Dict, Any, Optional
from app.services.llm_client import llm_client
from app.services.safety import safety_validator
from app.services.query_executor import query_executor
from app.services.explain_builder import explain_builder
from app.services.viz_inference import chart_inference_engine
from app.services.sessions import conversation_manager
from app.core.exceptions import NLQException, UnsafeQueryError

class NLQParser:
    """Main NLQ parser that orchestrates the conversion process"""
    
    def __init__(self):
        self.llm_client = llm_client
        self.safety_validator = safety_validator
        self.query_executor = query_executor
        self.explain_builder = explain_builder
        self.chart_inference_engine = chart_inference_engine
        self.conversation_manager = conversation_manager
    
    def parse_and_execute(self, prompt: str, conversation_id: Optional[str] = None, user_id: int = 1) -> Dict[str, Any]:
        """Parse NLQ and execute the resulting SQL"""
        
        try:
            # Get conversation context if available
            context = None
            if conversation_id:
                try:
                    context = self.conversation_manager.get_context_for_followup(conversation_id)
                except:
                    conversation_id = None  # Reset if conversation not found
            
            # Generate SQL using LLM
            llm_response = self.llm_client.generate_sql(prompt, context)
            sql = llm_response["sql"]
            explain = llm_response["explain"]
            
            # Validate SQL safety
            warnings = self.safety_validator.validate_query(sql)
            
            # Add LIMIT if missing
            sql = self.safety_validator.add_limit_if_missing(sql)
            
            # Execute query
            execution_result = self.query_executor.execute_query(sql)
            
            # Infer chart type
            chart_type = self.chart_inference_engine.infer_chart_type(
                execution_result["columns"],
                execution_result["rows"],
                sql
            )
            
            # Build explanation
            final_explain = self.explain_builder.build_explanation(sql)
            
            # Update conversation if applicable
            if conversation_id:
                self.conversation_manager.add_turn(conversation_id, prompt, sql, final_explain)
            else:
                # Create new conversation
                conversation_id = self.conversation_manager.create_conversation(user_id)
                self.conversation_manager.add_turn(conversation_id, prompt, sql, final_explain)
            
            return {
                "columns": execution_result["columns"],
                "rows": execution_result["rows"],
                "inferred_chart": chart_type,
                "explain": final_explain,
                "sql": sql,
                "warnings": warnings,
                "conversation_id": conversation_id
            }
            
        except UnsafeQueryError as e:
            raise NLQException(f"Unsafe query detected: {str(e)}")
        except Exception as e:
            raise NLQException(f"NLQ processing failed: {str(e)}")
    
    def parse_only(self, prompt: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """Parse NLQ to SQL without execution"""
        
        try:
            # Get conversation context if available
            context = None
            if conversation_id:
                try:
                    context = self.conversation_manager.get_context_for_followup(conversation_id)
                except:
                    conversation_id = None
            
            # Generate SQL using LLM
            llm_response = self.llm_client.generate_sql(prompt, context)
            sql = llm_response["sql"]
            explain = llm_response["explain"]
            
            # Validate SQL safety
            warnings = self.safety_validator.validate_query(sql)
            
            # Add LIMIT if missing
            sql = self.safety_validator.add_limit_if_missing(sql)
            
            # Build explanation
            final_explain = self.explain_builder.build_explanation(sql)
            
            return {
                "sql": sql,
                "warnings": warnings,
                "explain": final_explain,
                "conversation_id": conversation_id or "new"
            }
            
        except UnsafeQueryError as e:
            raise NLQException(f"Unsafe query detected: {str(e)}")
        except Exception as e:
            raise NLQException(f"NLQ parsing failed: {str(e)}")
    
    def execute_sql(self, sql: str) -> Dict[str, Any]:
        """Execute SQL query directly"""
        
        try:
            # Validate SQL safety
            warnings = self.safety_validator.validate_query(sql)
            
            # Add LIMIT if missing
            sql = self.safety_validator.add_limit_if_missing(sql)
            
            # Execute query
            execution_result = self.query_executor.execute_query(sql)
            
            # Infer chart type
            chart_type = self.chart_inference_engine.infer_chart_type(
                execution_result["columns"],
                execution_result["rows"],
                sql
            )
            
            return {
                "columns": execution_result["columns"],
                "rows": execution_result["rows"],
                "inferred_chart": chart_type,
                "warnings": warnings
            }
            
        except UnsafeQueryError as e:
            raise NLQException(f"Unsafe query detected: {str(e)}")
        except Exception as e:
            raise NLQException(f"SQL execution failed: {str(e)}")
    
    def refine_conversation(self, conversation_id: str, followup: str, user_id: int = 1) -> Dict[str, Any]:
        """Handle follow-up query in conversation context"""
        
        try:
            # Get refinement context
            refinement_context = self.conversation_manager.refine_query(conversation_id, followup)
            
            # Build refined prompt
            original_query = refinement_context["original_query"]
            refined_prompt = f"{original_query}. {followup}"
            
            # Parse and execute refined query
            return self.parse_and_execute(refined_prompt, conversation_id, user_id)
            
        except Exception as e:
            raise NLQException(f"Conversation refinement failed: {str(e)}")

# Global NLQ parser instance
nlq_parser = NLQParser()
