"""Main"""

from typing import List

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from digital_folder.api.api import api_router
from digital_folder.core.config import project_settings


def make_middleware() -> List[Middleware]:
    middlewares = []

    if project_settings.backend_cors_origins:
        middlewares = [
            Middleware(
                CORSMiddleware,
                allow_origins=[project_settings.backend_cors_origins],
                # allow_origins=[str(origin) for origin in project_settings.backend_cors_origins],
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
        docs_url="/",
        middleware=make_middleware(),
        swagger_ui_parameters={"docExpansion": "none"},
    )

    app.mount(
        "/static",
        StaticFiles(directory=project_settings.static_folder_path),
        name="static",
    )

    app.include_router(api_router, prefix="/api")

    return app
