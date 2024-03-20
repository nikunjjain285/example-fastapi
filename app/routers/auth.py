from fastapi import status,APIRouter,Depends,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import and_
from .. import schemas,utils,models,oauth2


router=APIRouter(tags=['Authentication'])

@router.post('/login',response_model=schemas.Token)
# user:schemas.UsersBase
def user_login(user:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    users=db.query(models.Users).filter(models.Users.email==user.username).first()
    if users==None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid credentials")
    if not utils.verify(user.password,users.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid credentials")
    else:
        access_token=oauth2.access_token_maker({"users_id":users.id})
        return {"access_token":access_token,"token_type":"bearer"}
