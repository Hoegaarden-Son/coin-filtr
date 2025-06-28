from fastapi import APIRouter, HTTPException
from models import YouTuber
from typing import List

router = APIRouter()

# 더미 유튜버 데이터
youtubers = [
    YouTuber(id=1, topic_id=1, name="캔들의신", channel_url="https://www.youtube.com/@godofcandle", like_count=12),
    YouTuber(id=2, topic_id=1, name="인범티비", channel_url="https://www.youtube.com/@inbumtv", like_count=5),
    YouTuber(id=3, topic_id=2, name="주억맨", channel_url="https://www.youtube.com/@jueokman", like_count=9),
]

@router.get("/{topic_id}", response_model=List[YouTuber])
def get_youtubers_for_topic(topic_id: int):
    return [yt for yt in youtubers if yt.topic_id == topic_id]

@router.get("/popular", response_model=List[YouTuber])
def get_popular_youtubers():
    return sorted(youtubers, key=lambda yt: yt.like_count, reverse=True)[:10]

@router.post("/{youtuber_id}/like")
def like_youtuber(youtuber_id: int):
    for yt in youtubers:
        if yt.id == youtuber_id:
            yt.like_count += 1
            return {"message": f"YouTuber {yt.name} liked!"}
    raise HTTPException(status_code=404, detail="YouTuber not found")
