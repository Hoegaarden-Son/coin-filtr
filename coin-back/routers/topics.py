from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models.global_tag import GlobalTag, TopicGlobalTag
from models.topic import Topic, TopicCreate, TopicUpdate, TopicRead
from typing import List, Optional

from services.global_tag_service import assign_all_global_tags_to_topic
from utils.slug import generate_unique_slug

router = APIRouter()


# GET /topics/
# GET /topics?search=bitcoin&tag=DeFi
# GET /topics?search=bitcoin → 이름/설명에 bitcoin이 포함된 토픽만
# GET /topics?tag=Ethereum → Ethereum 글로벌 태그가 연결된 토픽만
@router.get("/", response_model=List[TopicRead])
def get_topics(search: Optional[str] = None,
        tag: Optional[str] = None,
        session: Session = Depends(get_session),
    ):

    query = select(Topic)
    
    if search:
        query = query.where(Topic.name.contains(search))

    if tag:
        query = query.join(TopicGlobalTag).join(GlobalTag).where(GlobalTag.name == tag)

    results = session.exec(query).all()
    return results
    # return session.exec(select(Topic)).all()

# GET /topics/{id}
@router.get("/{topic_id}", response_model=Topic)
def get_topic(topic_id: int, session: Session = Depends(get_session)):
    topic = session.get(Topic, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

# POST /topics/
@router.post("/", response_model=TopicRead)
def create_topic(topic: TopicCreate, session: Session = Depends(get_session)):
    # ✅ 슬러그 자동 생성
    slug = generate_unique_slug(topic.name, session)
    
    topic_obj = Topic(
        name=topic.name,
        description=topic.description,
        slug=slug
    )

    # ✅ DB에 저장
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


@router.get("/slug/{slug}", response_model=Topic)
def get_topic_by_slug(slug: str, session: Session = Depends(get_session)):
    topic = session.exec(select(Topic).where(Topic.slug == slug)).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic