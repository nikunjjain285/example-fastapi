from pydantic import BaseModel,EmailStr
from datetime import datetime
from random import randrange
from typing import Optional

class PostBase(BaseModel):
    title : str
    content : str


class PostCreate(PostBase):
    pass

class UsersOutput(BaseModel):
    id:int
    email:str
    created_at:datetime

class Post(PostBase):
    id: int
    owner_id:int
    created_at: datetime
    owner: UsersOutput

    # class config:
        # orm_mode=True
class PostOut(BaseModel):
    Post:Post
    votes:int

    class config:
        orm_mode=True

class UsersBase(BaseModel):
    email:EmailStr
    password:str



class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[int]=None

class VotingInput(BaseModel):
    post_id: int
    votDir: int



