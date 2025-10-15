from fastapi import HTTPException, status

class NLQException(Exception):
    """Base exception for NLQ operations"""
    pass

class UnsafeQueryError(NLQException):
    """Raised when SQL query is deemed unsafe"""
    pass

class SchemaValidationError(NLQException):
    """Raised when schema validation fails"""
    pass

class LLMError(NLQException):
    """Raised when LLM operations fail"""
    pass

class ConversationNotFoundError(NLQException):
    """Raised when conversation is not found"""
    pass

class QueryExecutionError(NLQException):
    """Raised when query execution fails"""
    pass
