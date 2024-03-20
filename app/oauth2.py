from jose import jwt,JWTError
from datetime import datetime,timedelta
from . import schemas,database,models
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
# from .config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KEY ='09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM ='HS256'
# settings.access_token_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES =30
# settings.access_token_expiration_time

def access_token_maker(data:dict):
    to_encode=data.copy()
    expiration_time=datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expiration_time})
    access_token=jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return access_token

def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:int=payload.get("users_id")
        if id==None:
            raise credentials_exception
        else:
            token_data=schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
    
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="user not authorized",headers={"WWW-Authenticate":"Bearer"}) 
    token=verify_access_token(token,credentials_exception)
    user=db.query(models.Users).filter(models.Users.id==token.id).first()
    return user