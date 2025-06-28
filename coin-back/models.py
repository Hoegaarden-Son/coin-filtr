from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import List, Optional

# 주제 (ex: 비트코인, 이더리움 등)
class Topic(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# 태그
class Tag(BaseModel):
    id: int
    topic_id: int
    name: str
    like_count: int = 0
    is_popular: bool = False

# 사용자 즐겨찾기 (최대 3개)
class FavoriteTag(BaseModel):
    user_id: int
    tag_id: int

# 유저 추천용 YouTuber
class YouTuber(BaseModel):
    id: int
    topic_id: int
    name: str
    channel_url: str
    like_count: int = 0


class Video(BaseModel):
    id: str  # 유튜브 videoId
    topic_id: int
    title: str
    url: str
    summary: Optional[str] = None
    keywords: Optional[List[str]] = []