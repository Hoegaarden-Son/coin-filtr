from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import JSON
from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import List, Optional


class Topic(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None

class TopicCreate(SQLModel):
    name: str
    description: Optional[str] = None

class TopicUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None


# 태그
class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int
    name: str
    like_count: int = 0
    is_popular: bool = False

class TagCreate(SQLModel):
    topic_id: int
    name: str
    like_count: int = 0
    is_popular: bool = False

class TagUpdate(SQLModel):
    name: Optional[str] = None
    like_count: Optional[int] = None
    is_popular: Optional[bool] = None



# 사용자 즐겨찾기 (최대 3개)
class FavoriteTag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    tag_id: int

class FavoriteTagCreate(SQLModel):
    user_id: int
    tag_id: int

class FavoriteTagUpdate(SQLModel):  # Optional: 보통 필요 없음
    tag_id: Optional[int] = None



# 유튜버 추천
class YouTuber(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int
    name: str
    channel_url: str
    like_count: int = 0

class YouTuberCreate(SQLModel):
    topic_id: int
    name: str
    channel_url: str
    like_count: int = 0

class YouTuberUpdate(SQLModel):
    name: Optional[str] = None
    channel_url: Optional[str] = None
    like_count: Optional[int] = None


# 유튜브 영상
class Video(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int
    title: str
    url: str
    summary: Optional[str] = None
    # keywords: Optional[List[str]] = []
    keywords: Optional[List[str]] = Field(default_factory=list, sa_column=Column(JSON))

class VideoCreate(SQLModel):
    topic_id: int
    title: str
    url: str
    summary: Optional[str] = None
    keywords: Optional[List[str]] = []

class VideoUpdate(SQLModel):
    title: Optional[str] = None
    url: Optional[str] = None
    summary: Optional[str] = None
    keywords: Optional[List[str]] = None
