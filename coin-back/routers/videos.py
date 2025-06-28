from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from models.video import Video, VideoCreate, VideoUpdate
from database import get_session

router = APIRouter()

# 더미 비디오 데이터
# videos = [
#     Video(
#         id="abc123",
#         topic_id=1,
#         title="비트코인 차트 분석과 매수 타이밍",
#         url="https://youtube.com/watch?v=abc123",
#         summary="비트코인의 최근 하락 원인과 향후 반등 시나리오를 분석합니다.",
#         keywords=["차트", "매수", "비트코인"]
#     ),
#     Video(
#         id="def456",
#         topic_id=2,
#         title="이더리움 생태계와 디파이 전망",
#         url="https://youtube.com/watch?v=def456",
#         summary="이더리움의 스테이킹과 디파이 프로젝트들에 대한 개요.",
#         keywords=["디파이", "스테이킹", "이더리움"]
#     ),
# ]

# @router.get("/", response_model=List[Video])
# def get_videos(topic_id: Optional[int] = Query(None)):
#     if topic_id is not None:
#         return [v for v in videos if v.topic_id == topic_id]
#     return videos

# GET /videos/topic/{topic_id}
@router.get("/topic/{topic_id}", response_model=List[Video])
def get_videos_for_topic(topic_id: int, session: Session = Depends(get_session)):
    return session.exec(select(Video).where(Video.topic_id == topic_id)).all()

# GET /videos/
@router.get("/", response_model=List[Video])
def get_all_videos(session: Session = Depends(get_session)):
    return session.exec(select(Video)).all()

# POST /videos/
@router.post("/", response_model=Video)
def create_video(video_data: VideoCreate, session: Session = Depends(get_session)):
    video = Video.model_validate(video_data)
    session.add(video)
    session.commit()
    session.refresh(video)
    return video

# GET /videos/{video_id}
@router.get("/{video_id}", response_model=Video)
def get_video(video_id: int, session: Session = Depends(get_session)):
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

# PUT /videos/{video_id}
@router.put("/{video_id}", response_model=Video)
def update_video(video_id: int, video_data: VideoUpdate, session: Session = Depends(get_session)):
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    if video_data.title is not None:
        video.title = video_data.title
    if video_data.url is not None:
        video.url = video_data.url
    if video_data.summary is not None:
        video.summary = video_data.summary
    if video_data.keywords is not None:
        video.keywords = video_data.keywords

    session.commit()
    session.refresh(video)
    return video

# DELETE /videos/{video_id}
@router.delete("/{video_id}")
def delete_video(video_id: int, session: Session = Depends(get_session)):
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    session.delete(video)
    session.commit()
    return {"message": "Video deleted"}