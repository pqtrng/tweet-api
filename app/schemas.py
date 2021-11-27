from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint


class TweetBase(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        orm_mode = True


class TweetCreate(TweetBase):
    pass
