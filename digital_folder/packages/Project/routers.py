from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from digital_folder.core.pagination.types import PaginatedResponse
from digital_folder.core.pagination.utils import query_params_parser
from digital_folder.db.dependencies import get_db_validate_role, get_db_validate_user
from digital_folder.db.service import DbService
from digital_folder.packages.Project.dto import ProjectDTO
from digital_folder.packages.Project.schemas import (
    ProjectCreate,
    ProjectPatch,
    ProjectOut,
)

project_router = APIRouter()


class ProjectRouter:
    def __init__(self, router: APIRouter):
        self.model_dto = ProjectDTO
        self.router = router
        self.router.add_api_route("/list", self.list, methods=["GET"])
        self.router.add_api_route(
            "/project/{project_id}", self.get_by_id, methods=["GET"]
        )
        self.router.add_api_route("/create", self.create, methods=["POST"])
        self.router.add_api_route("/patch/{project_id}", self.patch, methods=["PATCH"])
        self.router.add_api_route(
            "/delete/{project_id}", self.delete, methods=["DELETE"]
        )

    async def list(
        self,
        filters: Optional[str] = Query(None, description="Comma-separated tag IDs"),
        search: Optional[str] = Query(None, description="Search string"),
        db: DbService = Depends(get_db_validate_user),
    ) -> PaginatedResponse:
        """List projects"""

        params = query_params_parser(
            db=db,
            filters=filters,
            search=search,
        )

        return self.model_dto(db).list(params)

    async def get_by_id(
        self,
        project_id: UUID,
        db: DbService = Depends(get_db_validate_user),
    ) -> ProjectOut:
        """Get project by id"""

        return self.model_dto(db).get_by_id(project_id)

    async def create(
        self,
        project: ProjectCreate,
        db: DbService = Depends(get_db_validate_role),
    ) -> ProjectOut:
        """Create project"""

        return self.model_dto(db).create(project)

    async def patch(
        self,
        project_id: UUID,
        project: ProjectPatch,
        db: DbService = Depends(get_db_validate_role),
    ) -> ProjectOut:
        """Edit project"""

        return self.model_dto(db).edit_by_id(project_id, project)

    async def delete(
        self,
        project_id: UUID,
        db: DbService = Depends(get_db_validate_role),
    ) -> None:
        """Delete project"""

        return self.model_dto(db).delete_by_id(project_id)


ProjectRouter(project_router)
