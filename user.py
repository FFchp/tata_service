from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import models, schemas
from hash import Hash
from database import get_db
from fastapi.exceptions import HTTPException

router = APIRouter(
    prefix = '/user',
    tags = ['User']
)

# Register
@router.post('/register', status_code = status.HTTP_201_CREATED)
def create(request: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    email = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        return {"msg" : "username is already used"}
    if email:
        return {"msg" : "Email is already used"}
    new_user = models.User(username = request.username, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#login
@router.post('/login')
def login(request: schemas.Login, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'Invalid Credentials')
    if Hash.verify(user.password, request.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'Incorrect Password')
    # generate a jwt token and return
    return user

# Delete User Ref by ID
@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete(id, db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    db.commit()
    return 'done'


# Update User
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_by_id(id, request: schemas.Update_User, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'User with id {id} not found')
    password = Hash.bcrypt(request.password)
    request.password = password
    user.update(request.dict())
    db.commit()
    return 'done'