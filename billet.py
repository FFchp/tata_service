from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.exceptions import HTTPException
import models, schemas, database

router = APIRouter(
    prefix = '/billet',
    tags = ['billet']
)

get_db = database.get_db

# add new billet
@router.post('/add', status_code = status.HTTP_201_CREATED)
def insert(request: schemas.billet, db: Session = Depends(get_db)):
    new_billet = models.billet(billet_no = request.billet_no, file_name = request.file_name, id = request.id)
    db.add(new_billet)
    db.commit()
    db.refresh(new_billet)
    return new_billet

# update billet (Config)
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def _update(id, request: schemas.billet, db: Session = Depends(get_db)):
    billet = db.query(models.billet).filter(models.billet.no == id).first()
    if not billet:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'billet with id {id} not found')
    billet.update(request.dict())
    db.commit()
    return 'done'

# query all billets
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.billet])
def querry_all_billet(db: Session = Depends(get_db)):
    billets = db.qurry(models.billet).order_by(models.billet.id).all()
    return billets

# search billet by billet_on
@router.get('/{billet_no}', status_code=status.HTTP_200_OK, response_model = List[schemas.billet])
def search_billet_no(billet_no, db: Session = Depends(get_db)):
    billets = db.query(models.billet).filter(models.billet.billet_no == billet_no).order_by(models.billet.timestamp).all()
    if not billets:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'billet with billet_on {billet_no} not found')
    return billets

# search billet by id 
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model = List[schemas.billet])
def search_billet_no(id, db: Session = Depends(get_db)):
    billets = db.query(models.billet).filter(models.billet.id == id).order_by(models.billet.timestamp).all()
    if not billets:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'billet with billet_on {id} not found')
    return billets

# search billet by Datatime
@router.get('/{datetime}', status_code=status.HTTP_200_OK, response_model=List[schemas.billet])
def search_billet_datatime(datetime, db: Session = Depends(get_db)):
    billets = db.query(models.billet).filter(models.billet.timestamp == datetime).order_by(models.billet.timestamp).all()
    if not billets:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'billet with billet_on {id} not found')
    return billets

# search billet by user
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=List[schemas.billet])
def search_billet_user(id, db: Session = Depends(get_db)):
    billets = db.query(models.billet).filter(models.billet.id == id).order_by(models.billet.id).all()
    if not billets:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'billet with billet_on {id} not found')
    return billets

