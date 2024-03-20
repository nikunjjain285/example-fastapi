from app.database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.sql.expression import null,text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import Relationship
class Post(Base):
    __tablename__="posts"
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default='True',nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete='CASCADE'),nullable=False)
    owner=Relationship("Users")

class Users(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    phone_no=Column(String,nullable=False)

class Vote(Base):
    __tablename__="votes"
    user_id=Column(Integer,ForeignKey("users.id",ondelete='CASCADE'),primary_key=True,nullable=False)
    post_id=Column(Integer,ForeignKey("posts.id",ondelete='CASCADE'),primary_key=True,nullable=False)
    


  