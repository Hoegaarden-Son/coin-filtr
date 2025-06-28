from sqlmodel import SQLModel, Field
from typing import Optional

class FavoriteTag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    tag_id: int

class FavoriteTagCreate(SQLModel):
    user_id: int
    tag_id: int

class FavoriteTagUpdate(SQLModel):
    tag_id: Optional[int] = None