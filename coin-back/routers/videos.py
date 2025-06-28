from fastapi import APIRouter, Query
from typing import List, Optional
from models import Video

router = APIRouter()

# 더미 비디오 데이터
videos = [
    Video(
        id="abc123",
        topic_id=1,
        title="비트코인 차트 분석과 매수 타이밍",
        url="https://youtube.com/watch?v=abc123",
        summary="비트코인의 최근 하락 원인과 향후 반등 시나리오를 분석합니다.",
        keywords=["차트", "매수", "비트코인"]
    ),
    Video(
        id="def456",
        topic_id=2,
        title="이더리움 생태계와 디파이 전망",
        url="https://youtube.com/watch?v=def456",
        summary="이더리움의 스테이킹과 디파이 프로젝트들에 대한 개요.",
        keywords=["디파이", "스테이킹", "이더리움"]
    ),
]

@router.get("/", response_model=List[Video])
def get_videos(topic_id: Optional[int] = Query(None)):
    if topic_id is not None:
        return [v for v in videos if v.topic_id == topic_id]
    return videos
