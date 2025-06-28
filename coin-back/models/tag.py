from sqlmodel import SQLModel, Field
from typing import Optional

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

