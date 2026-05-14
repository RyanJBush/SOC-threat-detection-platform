from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import get_current_user
from app.models import Event, User

router = APIRouter(prefix="/api/hunting", tags=["hunting"])


class SigmaLikeRule(BaseModel):
    title: str
    logsource: dict = Field(default_factory=dict)
    detection: dict
    condition: str


@router.post('/query')
def hunting_query(payload: SigmaLikeRule, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    selectors = payload.detection
    if payload.condition not in selectors:
        raise HTTPException(status_code=400, detail='condition must reference a detection selector key')

    selector = selectors[payload.condition]
    if not isinstance(selector, dict):
        raise HTTPException(status_code=400, detail='detection selector must be an object')

    query = db.query(Event).filter(Event.organization_id == current_user.organization_id)

    clauses = []
    for field, value in selector.items():
        if field == 'event_type':
            clauses.append(Event.event_type == value)
        elif field == 'source_ip':
            clauses.append(Event.source_ip == value)
        elif field == 'username':
            clauses.append(Event.username == value)
        elif field == 'severity':
            clauses.append(Event.severity == value)
        elif field == 'message_contains':
            clauses.append(Event.message.ilike(f"%{value}%"))
        elif field == 'status':
            clauses.append(Event.status == value)

    if clauses:
        query = query.filter(and_(*clauses))
    rows = query.order_by(Event.occurred_at.desc()).limit(200).all()
    return {'title': payload.title, 'count': len(rows), 'items': rows}
