from app.db.db import AsyncIOMotorClient, get_database
from app.schemas.auth import *
from fastapi import APIRouter, Depends, Response, Request
from app.api.controllers import auth as auth_controller


router = APIRouter()


@router.post("/register", response_model=RegisterResponse)
async def register(
    register_obj: Register,
    response: Response,
    db: AsyncIOMotorClient = Depends(get_database),
):
    res = await auth_controller.register(register_obj, db)
    response.status_code = 201
    return res


@router.post("/user/authenticate")
async def authenticate(
    email: str,
    request: Request,
    db: AsyncIOMotorClient = Depends(get_database),
):
    key = request.headers.get("api-key")
    print(key)

    auth_res = await auth_controller.authenticate(email, key, db)
    if auth_res:
        return {"message": "Authenticated"}


@router.get("/getUserData", response_model=GetUserDataRes)
async def getUserData(
    request: Request,
    response: Response,
    db: AsyncIOMotorClient = Depends(get_database),
):
    key = request.headers.get("api-key")
    auth_res = await auth_controller.get_user_data(key, db)

    return GetUserDataRes(**auth_res)
