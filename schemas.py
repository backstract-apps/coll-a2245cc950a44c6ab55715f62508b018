from pydantic import BaseModel

import datetime

import uuid

from typing import Any, Dict, List, Tuple

class Roles(BaseModel):
    role_id: int
    role_name: str


class ReadRoles(BaseModel):
    role_id: int
    role_name: str
    class Config:
        from_attributes = True


class Users(BaseModel):
    user_id: int
    username: str
    email: str
    role_id: int


class ReadUsers(BaseModel):
    user_id: int
    username: str
    email: str
    role_id: int
    class Config:
        from_attributes = True




class PostRoles(BaseModel):
    role_id: int
    role_name: str

    class Config:
        from_attributes = True



class PostUsers(BaseModel):
    user_id: int
    username: str
    email: str
    role_id: int

    class Config:
        from_attributes = True

