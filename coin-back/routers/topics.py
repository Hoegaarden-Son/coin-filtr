from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models.topic import Topic, TopicCreate, TopicUpdate
from typing import List

from services.global_tag_service import assign_all_global_tags_to_topic

router = APIRouter()

# 더미 데이터
# topics = [
#     Topic(id=1, name="비트코인", description="대표적인 암호화폐"),
#     Topic(id=2, name="이더리움", description="스마트 계약 플랫폼"),
# ]


# GET /topics/
@router.get("/", response_model=List[Topic])
def get_topics(session: Session = Depends(get_session)):
    return session.exec(select(Topic)).all()

# GET /topics/{id}
@router.get("/{topic_id}", response_model=Topic)
def get_topic(topic_id: int, session: Session = Depends(get_session)):
    topic = session.get(Topic, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

# POST /topics/
@router.post("/", response_model=Topic)
def create_topic(topic: Topic, session: Session = Depends(get_session)):
    topic_obj = Topic.model_validate(topic)

    session.add(topic_obj)
    session.commit()
    session.refresh(topic_obj)

    # ✅ 토픽 생성 직후 global 태그 연결
    assign_all_global_tags_to_topic(topic_obj.id, session)

    return topic_obj

# PUT /topics/{id}
@router.put("/{topic_id}", response_model=Topic)
def update_topic(topic_id: int, updated: Topic, session: Session = Depends(get_session)):
    topic = session.get(Topic, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    topic.name = updated.name
    topic.description = updated.description
    session.commit()
    session.refresh(topic)
    return topic

# DELETE /topics/{id}
@router.delete("/{topic_id}")
def delete_topic(topic_id: int, session: Session = Depends(get_session)):
    topic = session.get(Topic, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    session.delete(topic)
    session.commit()
    return {"message": "Topic deleted"}