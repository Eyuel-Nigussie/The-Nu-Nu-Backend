from .. import models, schemas, utils, oauth2
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine , get_db
from typing import List
router = APIRouter(
   prefix="/users",
    tags=["users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user : schemas.UserCreate, db: Session = Depends(get_db)):
   #user is the validated data the schema returns
   hashed_password = utils.hash(user.password) #hashing password
   user.password = hashed_password 
   new_user = models.User(
      **user.dict() # user is the the validated request, then we unpack it as dictionary (name=user.name, password=user.passwor, emai=user.email) then create a db user with that db
   )
   db.add(new_user)
   db.commit()
   db.refresh(new_user)
   return  new_user 


@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
   user = db.query(models.User).filter(models.User.id == id).first()
   if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id{id} does not exits")
   return user