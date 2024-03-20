from fastapi import Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import and_,func
from ..database import get_db
from typing import List,Optional
from .. import models,schemas,oauth2
# from ..config import settings

router=APIRouter(prefix='/posts',tags=['Posts'])


# Note these limit,skip and search are just query parameters that you may often see in urls
# @router.get('/',response_model=List[schemas.Post])
@router.get('/',response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db),user:dict=Depends(oauth2.get_current_user)
              ,limit:int=10,skip:int=0,search:Optional[str]=""):
    print(search)
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                                                                      models.Post.id==models.Vote.post_id).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db),user:dict=Depends(oauth2.get_current_user)):
    print(user.email)
    # post_data.update({'owner_id':user.id})
    new_post=models.Post(owner_id=user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get('/{id}',response_model=schemas.PostOut)
def get_onepost(id:int,db:Session=Depends(get_db),user:dict=Depends(oauth2.get_current_user)):
    post=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                                                                      models.Post.id==models.Vote.post_id).group_by(models.Post.id).filter(models.Post.id==id).first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with the id {id} cannot be found")
    else:
        return post


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),user:dict=Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(and_(models.Post.id==id,models.Post.owner_id==user.id))
    if models.Post.owner_id!=user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform the action bro")
    
    elif post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            ,detail=f"post with id {id} cannot be found")
    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}')
def update_posts(id:int,post:schemas.Post,db:Session=Depends(get_db)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    posts=post_query.first()
    if posts==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with the id {id} cannot be found")

    post_query.update({"title": "best places to visit in rainy season in India","content": "How are you doing here in this rain??"},synchronize_session=False)
    db.commit()
    return {'detial':'success'}


