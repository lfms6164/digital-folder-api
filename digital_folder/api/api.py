"""API routes"""

from fastapi import APIRouter

from digital_folder.packages.Group.routers import group_router
from digital_folder.packages.Project.routers import project_router
from digital_folder.packages.Server.routers import server_router
from digital_folder.packages.Tag.routers import tag_router
from digital_folder.packages.Ticket.routers import ticket_router
from digital_folder.packages.User.routers import user_router
from digital_folder.supabase.storage import supabase_router

api_router = APIRouter()

api_router.include_router(group_router, prefix="/groups", tags=["groups"])
api_router.include_router(project_router, prefix="/projects", tags=["projects"])
api_router.include_router(server_router, prefix="/server", tags=["server"])
api_router.include_router(tag_router, prefix="/tags", tags=["tags"])
api_router.include_router(ticket_router, prefix="/tickets", tags=["tickets"])
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(supabase_router, prefix="/supabase", tags=["supabase"])
