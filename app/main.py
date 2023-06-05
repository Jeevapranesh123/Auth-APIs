import sys
import re
import inspect

sys.dont_write_bytecode = True

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute
from loguru import logger
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.api import router as api_router
from app.core.config import settings

from app.db.db_utils import close_mongo_connection, connect_to_mongodb

app = FastAPI()

auth_required_routes = ["/auth/user/authenticate", "/auth/getUserData"]


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="1.0",
        description=settings.PROJECT_DESCRIPTION,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "api_key": {
            "type": "apiKey",
            "in": "header",
            "name": "api-key",
            "description": "Enter the API Key",
        }
    }

    # Get all routes where API Key should be passed in Header
    api_router = [route for route in app.routes if isinstance(route, APIRoute)]

    for route in api_router:
        path = getattr(route, "path")
        methods = [method.lower() for method in getattr(route, "methods")]
        for method in methods:
            if path in auth_required_routes:
                openapi_schema["paths"][path][method]["security"] = [{"api_key": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def ping():
    return {"ping": "pong"}


app.add_event_handler("startup", connect_to_mongodb)
app.add_event_handler("shutdown", close_mongo_connection)


@app.on_event("startup")
async def startup():
    logger.info("Application started")


app.include_router(api_router, prefix=settings.API_ROOT_PATH)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=4532,
        log_level="info",
        reload=True,
        workers=1,
    )
