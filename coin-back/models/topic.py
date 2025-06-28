from sqlmodel import SQLModel, Field
from typing import Optional

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