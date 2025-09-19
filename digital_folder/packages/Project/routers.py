from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Query

from digital_folder.helpers.utils import (
    query_params_parser,
    PaginatedResponse,
)
from digital_folder.packages.Project.dto import ProjectDTO
from digital_folder.packages.Project.schemas import (
    ProjectOut,
    ProjectCreate,
    ProjectPatch,
)

project_router = APIRouter()


class ProjectRouter:
    def __init__(self, router: APIRouter):
        self.model_dto = ProjectDTO()
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
    ) -> PaginatedResponse:
        """List projects"""

        params = query_params_parser(
            filters=filters,
            search=search,
        )

        return self.model_dto.list(params)

    async def get_by_id(self, project_id: UUID) -> ProjectOut:
        """Get project by id"""

        return self.model_dto.get_by_id(project_id)

    async def create(self, project: ProjectCreate) -> ProjectOut:
        """Create project"""

        return self.model_dto.create(project)

    async def patch(self, project_id: UUID, project: ProjectPatch) -> ProjectOut:
        """Edit project"""

        return self.model_dto.edit_by_id(project_id, project)

    async def delete(self, project_id: UUID) -> None:
        """Delete project"""

        return self.model_dto.delete_by_id(project_id)


ProjectRouter(project_router)
