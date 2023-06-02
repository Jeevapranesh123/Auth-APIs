from pydantic import BaseModel
from typing import Optional


class Register(BaseModel):
    username: str
    email: str


class RegisterResponse(BaseModel):
    username: str
    email: str
    uuid: str
    api_key: str


class RegisterInDB(Register):
    uuid: str
    expiry: int = 365  # Calculated in days


class GetUserDataRes(BaseModel):
    username: str
    email: str
