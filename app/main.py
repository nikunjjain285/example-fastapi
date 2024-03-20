from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import engine
from . import models
from app.routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)

app=FastAPI()

origins = [
    "https://www.google.com",
    "https://www.youtube.com",
    "https://fastapi.tiangolo.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/")
def get_aise():
    return {"Details":"Hello World!"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


    
