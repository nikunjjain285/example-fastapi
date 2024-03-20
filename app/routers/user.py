from fastapi import status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from .. import models,schemas,utils


router=APIRouter(prefix='/users',tags=['Users'])

@router.get('/')
def get_users(db:Session=Depends(get_db)):
    posts=db.query(models.Users).all()
    return {'detail':posts}


@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.UsersOutput)
def create_users(user:schemas.UsersBase,db:Session=Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}',response_model=schemas.UsersOutput)
def get_one_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.id==id).first()
    if user==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with the added id {id} could not be found")
    else:
        return user