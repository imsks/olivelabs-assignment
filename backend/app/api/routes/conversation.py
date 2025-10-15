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

class ConversationRefineRequest(BaseModel):
    conversation_id: str
    followup: str

class ConversationRefineResponse(BaseModel):
    columns: List[str]
    rows: List[List[Any]]
    inferred_chart: Optional[str]
    explain: Dict[str, Any]
    sql: str

@router.post("/refine", response_model=ConversationRefineResponse)
async def refine_conversation(
    request: ConversationRefineRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Handle follow-up queries in conversation context"""
    try:
        result = nlq_parser.refine_conversation(request.conversation_id, request.followup, current_user.id)
        return ConversationRefineResponse(**result)
    except NLQException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
