from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy import and_
from sqlalchemy.orm import Session
from ..database import get_db 
from .. import schemas,oauth2,models


router=APIRouter(prefix='/vote',tags=['Votes'])

@router.post('/')
def voting(vote:schemas.VotingInput,db:Session=Depends(get_db),current_user:dict=Depends(oauth2.get_current_user)):
    user_id=current_user.id
    # votes=vote.dict()
    voted=db.query(models.Vote).filter(and_(models.Vote.post_id==vote.post_id,models.Vote.user_id==user_id))
    if vote.votDir==0:
        if voted.first()==None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Voted post not found")
        else:
            voted.delete(synchronize_session=False)
            # db.refresh()
            db.commit()
            return {'detail':f'Vote has been removed'}
    elif vote.votDir==1:
        if voted.first()==None:
            votes=models.Vote(post_id=vote.post_id,user_id=user_id)
            db.add(votes)
            db.commit()
            db.refresh(votes)
            return {'detail':f'Vote has been added'}
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"You cannot like the same post again")
            


            
    

