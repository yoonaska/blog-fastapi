from pydantic import BaseModel
from typing import Optional


class BlogBase(BaseModel):
    title: str
    content: str

class BlogCreate(BlogBase):
    instance_id: Optional[int] = None

class Blog(BlogBase):
    id: int

    class Config:
        orm_mode = True
