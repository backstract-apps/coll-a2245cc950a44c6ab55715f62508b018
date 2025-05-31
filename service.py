from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, or_
from typing import *
from fastapi import Request, UploadFile, HTTPException
import models, schemas
import boto3
import jwt
import datetime
import requests
from pathlib import Path


async def post_file_upload(db: Session, document: UploadFile):

    bucket_name = "backstract-testing"
    region_name = "ap-south-1"
    file_path = "resources"

    s3_client = boto3.client(
        "s3",
        aws_access_key_id="AKIATET5D5CPSTHVVX25",
        aws_secret_access_key="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",
        aws_session_token=None,  # Optional, can be removed if not used
        region_name="ap-south-1",
    )

    # Read file content
    file_content = await document.read()

    name = document.filename
    file_path = file_path + "/" + name

    import mimetypes

    document.file.seek(0)
    s3_client.upload_fileobj(
        document.file,
        bucket_name,
        name,
        ExtraArgs={"ContentType": mimetypes.guess_type(name)[0]},
    )

    file_type = Path(document.filename).suffix
    file_size = 200

    file_url = f"https://{bucket_name}.s3.amazonaws.com/{name}"

    doc_file = file_url
    res = {
        "test": doc_file,
    }
    return res


async def get_roles(db: Session):

    query = db.query(models.Roles)

    roles_all = query.all()
    roles_all = (
        [new_data.to_dict() for new_data in roles_all] if roles_all else roles_all
    )
    res = {
        "roles_all": roles_all,
    }
    return res


async def get_roles_role_id(db: Session, role_id: int):

    query = db.query(models.Roles)
    query = query.filter(and_(models.Roles.role_id == role_id))

    roles_one = query.first()

    roles_one = (
        (roles_one.to_dict() if hasattr(roles_one, "to_dict") else vars(roles_one))
        if roles_one
        else roles_one
    )

    res = {
        "roles_one": roles_one,
    }
    return res


async def put_roles_role_id(db: Session, role_id: int, role_name: str):

    query = db.query(models.Roles)
    query = query.filter(and_(models.Roles.role_id == role_id))
    roles_edited_record = query.first()

    if roles_edited_record:
        for key, value in {"role_id": role_id, "role_name": role_name}.items():
            setattr(roles_edited_record, key, value)

        db.commit()
        db.refresh(roles_edited_record)

        roles_edited_record = (
            roles_edited_record.to_dict()
            if hasattr(roles_edited_record, "to_dict")
            else vars(roles_edited_record)
        )
    res = {
        "roles_edited_record": roles_edited_record,
    }
    return res


async def delete_roles_role_id(db: Session, role_id: int):

    query = db.query(models.Roles)
    query = query.filter(and_(models.Roles.role_id == role_id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        roles_deleted = record_to_delete.to_dict()
    else:
        roles_deleted = record_to_delete
    res = {
        "roles_deleted": roles_deleted,
    }
    return res


async def get_users(db: Session):

    query = db.query(models.Users)

    users_all = query.all()
    users_all = (
        [new_data.to_dict() for new_data in users_all] if users_all else users_all
    )
    res = {
        "users_all": users_all,
    }
    return res


async def get_users_user_id(db: Session, user_id: int):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.user_id == user_id))

    users_one = query.first()

    users_one = (
        (users_one.to_dict() if hasattr(users_one, "to_dict") else vars(users_one))
        if users_one
        else users_one
    )

    res = {
        "users_one": users_one,
    }
    return res


async def put_users_user_id(
    db: Session, user_id: int, username: str, email: str, role_id: int
):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.user_id == user_id))
    users_edited_record = query.first()

    if users_edited_record:
        for key, value in {
            "email": email,
            "role_id": role_id,
            "user_id": user_id,
            "username": username,
        }.items():
            setattr(users_edited_record, key, value)

        db.commit()
        db.refresh(users_edited_record)

        users_edited_record = (
            users_edited_record.to_dict()
            if hasattr(users_edited_record, "to_dict")
            else vars(users_edited_record)
        )
    res = {
        "users_edited_record": users_edited_record,
    }
    return res


async def delete_users_user_id(db: Session, user_id: int):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.user_id == user_id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        users_deleted = record_to_delete.to_dict()
    else:
        users_deleted = record_to_delete
    res = {
        "users_deleted": users_deleted,
    }
    return res


async def post_roles(db: Session, raw_data: schemas.PostRoles):
    role_id: int = raw_data.role_id
    role_name: str = raw_data.role_name

    record_to_be_added = {"role_id": role_id, "role_name": role_name}
    new_roles = models.Roles(**record_to_be_added)
    db.add(new_roles)
    db.commit()
    db.refresh(new_roles)
    roles_inserted_record = new_roles.to_dict()

    res = {
        "roles_inserted_record": roles_inserted_record,
    }
    return res


async def post_users(db: Session, raw_data: schemas.PostUsers):
    user_id: int = raw_data.user_id
    username: str = raw_data.username
    email: str = raw_data.email
    role_id: int = raw_data.role_id

    record_to_be_added = {
        "email": email,
        "role_id": role_id,
        "user_id": user_id,
        "username": username,
    }
    new_users = models.Users(**record_to_be_added)
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    users_inserted_record = new_users.to_dict()

    test = aliased(models.Roles)
    query = db.query(models.Users, test)

    query = query.join(test, and_(models.Users.username == models.Users.username))

    user_list = query.all()
    user_list = (
        [
            {
                "user_list_1": s1.to_dict() if hasattr(s1, "to_dict") else s1.__dict__,
                "user_list_2": s2.to_dict() if hasattr(s2, "to_dict") else s2.__dict__,
            }
            for s1, s2 in user_list
        ]
        if user_list
        else user_list
    )

    test = aliased(models.Users)
    query = db.query(models.Roles, test)

    query = query.join(test, and_(models.Roles.role_id == models.Roles.role_id))

    user_list1 = query.all()
    user_list1 = (
        [
            {
                "user_list1_1": s1.to_dict() if hasattr(s1, "to_dict") else s1.__dict__,
                "user_list1_2": s2.to_dict() if hasattr(s2, "to_dict") else s2.__dict__,
            }
            for s1, s2 in user_list1
        ]
        if user_list1
        else user_list1
    )

    test = aliased(models.Users)
    query = db.query(models.Users, test)

    query = query.join(test, and_(models.Users.username == models.Users.email))

    test1 = query.all()
    test1 = (
        [
            {
                "test1_1": s1.to_dict() if hasattr(s1, "to_dict") else s1.__dict__,
                "test1_2": s2.to_dict() if hasattr(s2, "to_dict") else s2.__dict__,
            }
            for s1, s2 in test1
        ]
        if test1
        else test1
    )
    res = {
        "users_inserted_record": users_inserted_record,
        "user_list": user_list,
        "user_list1": user_list1,
        "test1": test1,
    }
    return res
