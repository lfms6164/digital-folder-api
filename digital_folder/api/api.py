"""API routes"""

from fastapi import APIRouter


from digital_folder.packages.auth.routers import auth_router
from digital_folder.packages.Project.routers import project_router
from digital_folder.packages.Tag.routers import tag_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(project_router, prefix="/projects", tags=["projects"])
api_router.include_router(tag_router, prefix="/tags", tags=["tags"])
