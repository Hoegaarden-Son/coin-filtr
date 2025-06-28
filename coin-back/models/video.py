from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import JSON
from typing import List, Optional

class Video(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int
    title: str
    url: str
    summary: Optional[str] = None
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