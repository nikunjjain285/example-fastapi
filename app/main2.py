from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .database import engine,get_db
from . import models,schemas,utils
from routers import post,user

models.Base.metadata.create_all(bind=engine)

app=FastAPI()



while True:
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='PLrisk@123'
                          ,cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print('Successfully connected to the database')
        break
    except Exception as error:
        print(f'Failed to connect to the database because of the error {error}')
        time.sleep(5)


# The statement that starts from '@' is the decorator that uses your Fastapi interface and reuired http method 
# same path operation runs in order the one which will meet the criteria first will be executed firstly.


my_posts=[{'title':'My life my rules','content':'Be Happy','id':1},
          {'title':'I love sweetpotato','content':'At MG Road','id':2}]

def find_post(id):
    id=int(id)
    cursor.execute(f"""select * from posts where id=%s""",(str(id)))
    p=cursor.fetchone()
    # for p in my_posts:
    #     if p['id']==id:
    return p

def find_index_id(id):
    for i,j in enumerate(my_posts):
        if j['id']==id:
            return i


@app.get('/')
def read_root():
    return {'Hello':'Welcome to my first api!!!!!s'}


@app.get('/sqlalchemy')
def test_sqlalchemy(db:Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return {'data':posts}

@app.get('/posts',response_model=list[schemas.PostCreate])
def get_posts(db:Session=Depends(get_db)):
    # cursor.execute('''SELECT * from posts''')
    # posts=cursor.fetchall()
    posts=db.query(models.Post).all()
    return posts


@app.get('/users')
def get_users(db:Session=Depends(get_db)):
    posts=db.query(models.Users).all()
    return {'detail':posts}


@app.post('/users',status_code=status.HTTP_201_CREATED,response_model=schemas.UsersOutput)
def create_users(user:schemas.UsersBase,db:Session=Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/users/{id}',response_model=schemas.UsersOutput)
def get_one_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.id==id).first()
    if user==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with the added id {id} could not be found")
    else:
        return user

@app.post('/createpost')
def create_posts(payload: dict=Body(...)):
    print(payload)
    return {'Post':f"Your post has been created with title {payload['title']}"}


@app.post('/posts',status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db)):
    # print(post)
    # print(post.title)
    # post_dict=post.dict()
    # post_dict['id']=randrange(0,1000000)
    # my_posts.append(post_dict)
    # cursor.execute("""insert into posts(id,title,content) values(%s,%s,%s) returning * """,(post.id,post.title,post.content))
    # new_post=cursor.fetchone()
    # conn.commit()
    new_post=models.Post(**post.dict())
    # new_post=models.Post(id=post.id,title=post.title,content=post.content,published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {'Data':new_post}
    



@app.get('/posts/latest')
def post_latest():
    posti=my_posts[len(my_posts)-1]
    return {"detial":posti}



@app.get('/posts/{id}')
def get_onepost(id:int,db:Session=Depends(get_db)):
    # post=find_post(id)
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with the id {id} could not be found")
    #     # response.status_code=status.HTTP_404_NOT_FOUND
    #     # return {'message':f"post with id {id} cannot be found"}
    post=db.query(models.Post).filter(models.Post.id==id).first()
    return {'your_post':post}


@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):
    # index=find_index_id(id)
    # cursor.execute("""delete from posts where id=%s returning *""",(str(id)))
    # post=cursor.fetchone()
    # conn.commit()
    post=db.query(models.Post).filter(models.Post.id==id)
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            ,detail=f"post with id {id} cannot be found")
    # my_posts.pop(index)
    # return {'detial':"your post has been deleted"}
    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_posts(id:int,post:schemas.Post,db:Session=Depends(get_db)):
    # index=find_index_id(id)
    # post_dict=post.dict()
    # post_dict['id']=id
    # my_posts[index]=post_dict
    # cursor.execute("""update posts set title=%s,content=%s where id=%s returning *""",(post.title,post.content,str(id)))
    # posts=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    posts=post_query.first()
    if posts==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with the id {id} cannot be found")

    post_query.update({"title": "best places to visit in rainy season in India","content": "How are you doing here in this rain??"},synchronize_session=False)
    db.commit()
    return {'detial':'success'}


@app.patch('/posts/{id}')
def update_posts(id:int,post:schemas.Post):
    index=find_index_id(id)
    post_dict=post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with the id {id} cannot be found")
    return {'detial':post}


    
