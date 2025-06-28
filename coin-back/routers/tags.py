from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.tag import Tag, TagCreate, TagUpdate
from database import get_session

router = APIRouter()

# 더미 태그 데이터
# tags = [
#     Tag(id=1, topic_id=1, name="차트분석", like_count=5),
#     Tag(id=2, topic_id=1, name="심리분석", like_count=2),
#     Tag(id=3, topic_id=2, name="디파이", like_count=3),
# ]

# GET /tags/topic/{topic_id}
@router.get("/topic/{topic_id}", response_model=List[Tag])
def get_tags_for_topic(topic_id: int, session: Session = Depends(get_session)):
    return session.exec(select(Tag).where(Tag.topic_id == topic_id)).all()

# GET /tags/popular
@router.get("/popular", response_model=List[Tag])
def get_popular_tags(session: Session = Depends(get_session)):
    return session.exec(
        select(Tag).order_by(Tag.like_count.desc()).limit(10)
    ).all()

# POST /tags/
@router.post("/", response_model=Tag)
def create_tag(tag_data: TagCreate, session: Session = Depends(get_session)):
    tag = Tag.model_validate(tag_data)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag

# POST /tags/{tag_id}/like
@router.post("/{tag_id}/like", response_model=Tag)
def like_tag(tag_id: int, session: Session = Depends(get_session)):
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag.like_count += 1
    session.commit()
    session.refresh(tag)
    return tag


# PUT /tags/{tag_id}
@router.put("/{tag_id}", response_model=Tag)
def update_tag(tag_id: int, tag_data: TagUpdate, session: Session = Depends(get_session)):
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    tag.name = tag_data.name or tag.name
    tag.like_count = tag_data.like_count if tag_data.like_count is not None else tag.like_count
    tag.is_popular = tag_data.is_popular if tag_data.is_popular is not None else tag.is_popular

    session.commit()
    session.refresh(tag)
    return tag

# DELETE /tags/{tag_id}
@router.delete("/{tag_id}")
def delete_tag(tag_id: int, session: Session = Depends(get_session)):
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    session.delete(tag)
    session.commit()
    return {"message": "Tag deleted"}
