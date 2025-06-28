from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from models.youtuber import YouTuber, YouTuberCreate, YouTuberUpdate
from database import get_session

router = APIRouter()

# 더미 유튜버 데이터
# youtubers = [
#     YouTuber(id=1, topic_id=1, name="캔들의신", channel_url="https://www.youtube.com/@godofcandle", like_count=12),
#     YouTuber(id=2, topic_id=1, name="인범티비", channel_url="https://www.youtube.com/@inbumtv", like_count=5),
#     YouTuber(id=3, topic_id=2, name="주억맨", channel_url="https://www.youtube.com/@jueokman", like_count=9),
# ]

# GET /youtubers/topic/{topic_id}
@router.get("/topic/{topic_id}", response_model=List[YouTuber])
def get_youtubers_for_topic(topic_id: int, session: Session = Depends(get_session)):
    return session.exec(select(YouTuber).where(YouTuber.topic_id == topic_id)).all()

# GET /youtubers/popular
@router.get("/popular", response_model=List[YouTuber])
def get_popular_youtubers(session: Session = Depends(get_session)):
    return session.exec(
        select(YouTuber).order_by(YouTuber.like_count.desc()).limit(10)
    ).all()

# POST /youtubers/{youtuber_id}/like
@router.post("/{youtuber_id}/like")
def like_youtuber(youtuber_id: int, session: Session = Depends(get_session)):
    yt = session.get(YouTuber, youtuber_id)
    if not yt:
        raise HTTPException(status_code=404, detail="YouTuber not found")
    yt.like_count += 1
    session.commit()
    return {"message": f"YouTuber '{yt.name}' liked!", "like_count": yt.like_count}

# 아래는 일반 CRUD도 같이 제공
@router.get("/", response_model=List[YouTuber])
def get_all_youtubers(session: Session = Depends(get_session)):
    return session.exec(select(YouTuber)).all()

@router.get("/{youtuber_id}", response_model=YouTuber)
def get_youtuber(youtuber_id: int, session: Session = Depends(get_session)):
    yt = session.get(YouTuber, youtuber_id)
    if not yt:
        raise HTTPException(status_code=404, detail="YouTuber not found")
    return yt

@router.post("/", response_model=YouTuber)
def create_youtuber(data: YouTuberCreate, session: Session = Depends(get_session)):
    yt = YouTuber.model_validate(data)
    session.add(yt)
    session.commit()
    session.refresh(yt)
    return yt

@router.put("/{youtuber_id}", response_model=YouTuber)
def update_youtuber(youtuber_id: int, data: YouTuberUpdate, session: Session = Depends(get_session)):
    yt = session.get(YouTuber, youtuber_id)
    if not yt:
        raise HTTPException(status_code=404, detail="YouTuber not found")

    yt.name = data.name or yt.name
    yt.channel_url = data.channel_url or yt.channel_url
    yt.like_count = data.like_count if data.like_count is not None else yt.like_count

    session.commit()
    session.refresh(yt)
    return yt

@router.delete("/{youtuber_id}")
def delete_youtuber(youtuber_id: int, session: Session = Depends(get_session)):
    yt = session.get(YouTuber, youtuber_id)
    if not yt:
        raise HTTPException(status_code=404, detail="YouTuber not found")
    session.delete(yt)
    session.commit()
    return {"message": "YouTuber deleted"}