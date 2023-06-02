import datetime
import random
import string
from uuid import uuid4
from app.db.db_utils import AsyncIOMotorClient
from app.schemas.auth import *
from fastapi import HTTPException
from app.core.config import settings


async def check_existing_email(
    email: str,
    conn: AsyncIOMotorClient,
):
    data = await conn[settings.MONGO_PROD_DATABASE][
        settings.MONGO_USERS_COLLECTION_NAME
    ].find_one({"email": email})
    if data:
        return True
    return False


async def check_existing_username(
    username: int,
    conn: AsyncIOMotorClient,
):
    data = await conn[settings.MONGO_PROD_DATABASE][
        settings.MONGO_USERS_COLLECTION_NAME
    ].find_one({"username": username})
    if data:
        return True
    return False


async def register(register_obj, conn: AsyncIOMotorClient):
    data = {
        "uuid": str(uuid4()).replace("-", ""),
        "username": register_obj.username,
        "email": register_obj.email,
    }

    reg_db = RegisterInDB(**data)

    res = await conn[settings.MONGO_PROD_DATABASE][
        settings.MONGO_USERS_COLLECTION_NAME
    ].insert_one(reg_db.dict())

    if res:
        return reg_db
    return False


async def store_api_key(uuid, key, db):
    data = {
        "uuid": uuid,
        "api_key": key,
        "expiry": datetime.datetime.now()
        + datetime.timedelta(days=1),  # Expire the key in 1 day
    }

    res = await db[settings.MONGO_PROD_DATABASE][
        settings.MONGO_KEYS_COLLECTION_NAME
    ].insert_one(data)

    if res:
        return True
    return False


async def get_uuid_from_key(key, db):
    data = await db[settings.MONGO_PROD_DATABASE][
        settings.MONGO_KEYS_COLLECTION_NAME
    ].find_one({"api_key": key})
    print(data)
    if data:
        return data
    return False


async def get_user_from_uuid(uuid, db):
    data = await db[settings.MONGO_PROD_DATABASE][
        settings.MONGO_USERS_COLLECTION_NAME
    ].find_one({"uuid": uuid})

    if data:
        return data
    return False
