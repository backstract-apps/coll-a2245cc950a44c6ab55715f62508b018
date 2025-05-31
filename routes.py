from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List
import service, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/file_upload')
async def post_file_upload(document: UploadFile, db: Session = Depends(get_db)):
    try:
        return await service.post_file_upload(db, document)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/roles/')
async def get_roles(db: Session = Depends(get_db)):
    try:
        return await service.get_roles(db)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/roles/role_id')
async def get_roles_role_id(role_id: int, db: Session = Depends(get_db)):
    try:
        return await service.get_roles_role_id(db, role_id)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/roles/role_id/')
async def put_roles_role_id(role_id: int, role_name: str, db: Session = Depends(get_db)):
    try:
        return await service.put_roles_role_id(db, role_id, role_name)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/roles/role_id')
async def delete_roles_role_id(role_id: int, db: Session = Depends(get_db)):
    try:
        return await service.delete_roles_role_id(db, role_id)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/users/')
async def get_users(db: Session = Depends(get_db)):
    try:
        return await service.get_users(db)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/users/user_id')
async def get_users_user_id(user_id: int, db: Session = Depends(get_db)):
    try:
        return await service.get_users_user_id(db, user_id)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/users/user_id/')
async def put_users_user_id(user_id: int, username: str, email: str, role_id: int, db: Session = Depends(get_db)):
    try:
        return await service.put_users_user_id(db, user_id, username, email, role_id)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/users/user_id')
async def delete_users_user_id(user_id: int, db: Session = Depends(get_db)):
    try:
        return await service.delete_users_user_id(db, user_id)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/roles/')
async def post_roles(raw_data: schemas.PostRoles, db: Session = Depends(get_db)):
    try:
        return await service.post_roles(db, raw_data)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/users/')
async def post_users(raw_data: schemas.PostUsers, db: Session = Depends(get_db)):
    try:
        return await service.post_users(db, raw_data)
    except Exception as e:
        raise HTTPException(500, str(e))

