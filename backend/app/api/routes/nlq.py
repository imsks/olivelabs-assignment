from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.conversation import User
from app.services.nlq_parser import nlq_parser
from app.core.exceptions import NLQException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

router = APIRouter()

class NLQParseRequest(BaseModel):
    prompt: str
    conversation_id: Optional[str] = None

class NLQParseResponse(BaseModel):
    sql: str
    warnings: List[str]
    explain: Dict[str, Any]
    conversation_id: str

class NLQExecuteRequest(BaseModel):
    sql: str
    result_format: str = "table"

class NLQExecuteResponse(BaseModel):
    columns: List[str]
    rows: List[List[Any]]
    inferred_chart: Optional[str]

class NLQQueryRequest(BaseModel):
    prompt: str
    conversation_id: Optional[str] = None

class NLQQueryResponse(BaseModel):
    columns: List[str]
    rows: List[List[Any]]
    inferred_chart: Optional[str]
    explain: Dict[str, Any]
    sql: str

@router.post("/parse", response_model=NLQParseResponse)
async def parse_nlq(
    request: NLQParseRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Parse natural language query to SQL"""
    try:
        result = nlq_parser.parse_only(request.prompt, request.conversation_id)
        return NLQParseResponse(**result)
    except NLQException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/execute", response_model=NLQExecuteResponse)
async def execute_sql(
    request: NLQExecuteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Execute SQL query"""
    try:
        result = nlq_parser.execute_sql(request.sql)
        return NLQExecuteResponse(**result)
    except NLQException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/query", response_model=NLQQueryResponse)
async def query_nlq(
    request: NLQQueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Combined parse and execute endpoint"""
    try:
        result = nlq_parser.parse_and_execute(request.prompt, request.conversation_id, current_user.id)
        return NLQQueryResponse(**result)
    except NLQException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
