from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.global_tag import GlobalTag, TopicGlobalTag
from models.topic import Topic
from database import get_session
from typing import List

from services.global_tag_service import assign_all_global_tags_to_topic, assign_global_tag_to_all_topics

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

    # ✅ 모든 topic에 자동 연결!
    assign_global_tag_to_all_topics(tag.id, session)

    return tag

@router.put("/{global_tag_id}", response_model=GlobalTag)
def update_global_tag(global_tag_id: int, update: GlobalTag, session: Session = Depends(get_session)):
    tag = session.get(GlobalTag, global_tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="GlobalTag not found")
    tag.name = update.name
    tag.description = update.description
    session.commit()
    session.refresh(tag)
    return tag

@router.delete("/{global_tag_id}")
def delete_global_tag(global_tag_id: int, session: Session = Depends(get_session)):
    tag = session.get(GlobalTag, global_tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="GlobalTag not found")
    session.delete(tag)
    session.commit()
    return {"message": "Deleted"}


@router.get("/topic/{topic_id}")
def get_global_tags_for_topic(topic_id: int, session: Session = Depends(get_session)):
    stmt = select(TopicGlobalTag, GlobalTag).where(
        TopicGlobalTag.topic_id == topic_id,
        TopicGlobalTag.global_tag_id == GlobalTag.id
    )
    results = session.exec(stmt).all()

    return [
        {
            "id": tag.id,
            "name": tag.name,
            "description": tag.description,
            "like_count": link.like_count
        }
        for link, tag in results
    ]


@router.post("/global-tags/topic/{topic_id}/assign-all")
def assign_all(topic_id: int, session: Session = Depends(get_session)):
    assign_all_global_tags_to_topic(topic_id, session)
    return {"message": f"Global tags assigned to topic {topic_id}"}

@router.post("/topics/{topic_id}/global-tags/{tag_id}/like")
def like_global_tag_in_topic(topic_id: int, tag_id: int, session: Session = Depends(get_session)):
    link = session.get(TopicGlobalTag, (topic_id, tag_id))
    if not link:
        raise HTTPException(status_code=404, detail="해당 토픽/태그 연결이 없습니다.")

    link.like_count += 1
    session.commit()
    session.refresh(link)
    return {
        # "message": "좋아요 완료", 
        "message": f"'{link.topic_id}'번 토픽의 '{link.global_tag_id}'번 태그 좋아요 완료",
        "like_count": link.like_count
    }



@router.get("/tags/global/stats")
def get_global_tag_stats(session: Session = Depends(get_session)):
    stmt = select(TopicGlobalTag, GlobalTag, Topic).where(
        TopicGlobalTag.global_tag_id == GlobalTag.id,
        TopicGlobalTag.topic_id == Topic.id
    )
    results = session.exec(stmt).all()

    grouped = {}

    for link, tag, topic in results:
        if tag.id not in grouped:
            grouped[tag.id] = {
                "name": tag.name,
                "description": tag.description,
                "stats": []
            }

        grouped[tag.id]["stats"].append({
            "topic_id": topic.id,
            "topic_name": topic.name,
            "like_count": link.like_count
        })

    return list(grouped.values())