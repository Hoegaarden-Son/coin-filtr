from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.global_tag import GlobalTag, TopicGlobalTag
from database import get_session
from typing import List

router = APIRouter()

# CRUD
@router.get("/", response_model=List[GlobalTag])
def list_global_tags(session: Session = Depends(get_session)):
    return session.exec(select(GlobalTag)).all()

@router.post("/", response_model=GlobalTag)
def create_global_tag(tag: GlobalTag, session: Session = Depends(get_session)):
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag

@router.put("/{tag_id}", response_model=GlobalTag)
def update_global_tag(tag_id: int, update: GlobalTag, session: Session = Depends(get_session)):
    tag = session.get(GlobalTag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="GlobalTag not found")
    tag.name = update.name
    tag.description = update.description
    session.commit()
    session.refresh(tag)
    return tag

@router.delete("/{tag_id}")
def delete_global_tag(tag_id: int, session: Session = Depends(get_session)):
    tag = session.get(GlobalTag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="GlobalTag not found")
    session.delete(tag)
    session.commit()
    return {"message": "Deleted"}
