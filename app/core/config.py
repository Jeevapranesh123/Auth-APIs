import logging
from os import environ as env
from typing import List

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(".env")


class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS: List = [
        "*",
    ]

    PROJECT_NAME: str = env.get("PROJECT_NAME")
    PROJECT_DESCRIPTION: str = env.get("PROJECT_DESCRIPTION")
    API_ROOT_PATH: str = env.get("API_ROOT_PATH", "")

    MONGODB_URL: str = env.get("MONGODB_URL")
    MONGO_USERS_COLLECTION_NAME: str = "users"
    MONGO_KEYS_COLLECTION_NAME: str = "keys"
    MONGO_PROD_DATABASE: str = env.get("MONGO_PROD_DATABASE")

    class Config:
        case_sensitive = True


settings = Settings()
env_with_secrets = env
