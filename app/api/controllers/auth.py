from app.db.db_utils import AsyncIOMotorClient
from fastapi import HTTPException
from app.schemas.auth import *
from app.crud import auth as auth_crud
import secrets
import datetime


async def register(register_obj: Register, db: AsyncIOMotorClient):
    if await auth_crud.check_existing_email(register_obj.email, db):
        raise HTTPException(
            status_code=422,
            detail="Email Already exists",
        )

    if await auth_crud.check_existing_username(register_obj.username, db):
        raise HTTPException(
            status_code=422,
            detail="Mobile Already exists",
        )

    user = await auth_crud.register(register_obj, db)

    if user:
        key = await gen_api_key(10)
        if await auth_crud.store_api_key(user.uuid, key, db):
            return RegisterResponse(**user.dict(), api_key=key)

    raise HTTPException(
        status_code=500,
        detail="Something went wrong",
    )


async def gen_api_key(length):
    api_key = secrets.token_urlsafe(length)
    return api_key


async def authenticate(email, key, db: AsyncIOMotorClient):
    uuid = await auth_crud.get_uuid_from_key(key, db)

    if not uuid:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    user = await auth_crud.get_user_from_uuid(uuid["uuid"], db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    if user["email"] != email:
        raise HTTPException(status_code=401, detail="Invalid User")

    return user


async def get_user_data(key, db: AsyncIOMotorClient):
    uuid = await auth_crud.get_uuid_from_key(key, db)

    if not uuid:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    if uuid["expiry"] < datetime.datetime.now():
        raise HTTPException(status_code=401, detail="API Key Expired")

    user = await auth_crud.get_user_from_uuid(uuid["uuid"], db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return user
