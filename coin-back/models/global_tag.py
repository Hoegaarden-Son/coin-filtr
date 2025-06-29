from sqlmodel import SQLModel, Field
from typing import Optional

class GlobalTag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None

class GlobalTagCreate(SQLModel):
    name: str
    description: Optional[str] = None  

class GlobalTagUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None


# Composite Primary Key Mdodel For Topic and GlobalTag Relationship
class TopicGlobalTag(SQLModel, table=True):
    topic_id: int = Field(foreign_key="topic.id", primary_key=True)
    global_tag_id: int = Field(foreign_key="globaltag.id", primary_key=True)
    like_count: int = 0


