"""Main"""

from typing import List

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from digital_folder.api.api import api_router
from digital_folder.core.config import project_settings


def make_middleware() -> List[Middleware]:
    middlewares = []

    if project_settings.backend_cors_origins:
        middlewares = [
            Middleware(
                CORSMiddleware,
                allow_origins=project_settings.backend_cors_origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            ),
        ]

    return middlewares


def create_app() -> FastAPI:
    app = FastAPI(
        title=project_settings.project_name,
        version=project_settings.project_version,
        docs_url="/" if project_settings.env.lower() != "prod" else None,
        middleware=make_middleware(),
        swagger_ui_parameters={"docExpansion": "none"},
    )

    app.include_router(api_router, prefix="/api")

    return app
