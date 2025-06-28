from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import JSON
from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import List, Optional


# 주제 (ex: 비트코인, 이더리움 등)
class Topic(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None


# 태그
class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int
    name: str
    like_count: int = 0
    is_popular: bool = False


# 사용자 즐겨찾기 (최대 3개)
class FavoriteTag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    tag_id: int


# 유튜버 추천
class YouTuber(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int
    name: str
    channel_url: str
    like_count: int = 0


# 유튜브 영상
class Video(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int
    title: str
    url: str
    summary: Optional[str] = None
    # keywords: Optional[List[str]] = []
    keywords: Optional[List[str]] = Field(default_factory=list, sa_column=Column(JSON))


# # 주제 (ex: 비트코인, 이더리움 등)
# class Topic(BaseModel):
#     id: int
#     name: str
#     description: Optional[str] = None

# # 태그
# class Tag(BaseModel):
#     id: int
#     topic_id: int
#     name: str
#     like_count: int = 0
#     is_popular: bool = False

# # 사용자 즐겨찾기 (최대 3개)
# class FavoriteTag(BaseModel):
#     user_id: int
#     tag_id: int

# # 유저 추천용 YouTuber
# class YouTuber(BaseModel):
#     id: int
#     topic_id: int
#     name: str
#     channel_url: str
#     like_count: int = 0


# class Video(BaseModel):
#     id: str  # 유튜브 videoId
#     topic_id: int
#     title: str
#     url: str
#     summary: Optional[str] = None
#     keywords: Optional[List[str]] = []