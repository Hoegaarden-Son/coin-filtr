from typing import List
from fastapi import APIRouter, HTTPException
from models import Tag

router = APIRouter()

# 더미 태그 데이터
tags = [
    Tag(id=1, topic_id=1, name="차트분석", like_count=5),
    Tag(id=2, topic_id=1, name="심리분석", like_count=2),
    Tag(id=3, topic_id=2, name="디파이", like_count=3),
]


@router.get("/popular", response_model=List[Tag])
def get_popular_tags():
    return sorted(tags, key=lambda t: t.like_count, reverse=True)[:10]

@router.get("/{topic_id}", response_model=List[Tag])
def get_tags_for_topic(topic_id: int):
    return [tag for tag in tags if tag.topic_id == topic_id]

@router.post("/{tag_id}/like")
def like_tag(tag_id: int):
    for tag in tags:
        if tag.id == tag_id:
            tag.like_count += 1
            return {"message": f"Tag {tag.name} liked!"}
    raise HTTPException(status_code=404, detail="Tag not found")
