from sqlmodel import SQLModel, Field
from typing import Optional

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