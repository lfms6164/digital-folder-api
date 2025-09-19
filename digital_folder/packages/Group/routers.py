from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Query

from digital_folder.helpers.utils import query_params_parser, PaginatedResponse
from digital_folder.packages.Group.dto import GroupDTO
from digital_folder.packages.Group.schemas import (
    GroupCreate,
    GroupOut,
    GroupPatch,
)

group_router = APIRouter()


class GroupRouter:
    def __init__(self, router: APIRouter):
        self.model_dto = GroupDTO()
        self.router = router
        self.router.add_api_route("/list", self.list, methods=["GET"])
        self.router.add_api_route("/create", self.create, methods=["POST"])
        self.router.add_api_route("/patch/{group_id}", self.patch, methods=["PATCH"])
        self.router.add_api_route("/delete/{group_id}", self.delete, methods=["DELETE"])

    async def list(
        self,
        filters: Optional[str] = Query(None, description="Comma-separated filter data"),
        items_per_page: int = Query(
            10,
            ge=-1,
            le=100,
            description="-1 returns all the items",
            alias="itemsPerPage",
        ),
        page: int = Query(1, ge=1),
        search: Optional[str] = Query(None, description="Search string"),
        sort_by: Optional[str] = Query(
            None,
            description="""JSON string like [{"key":"name","order":"desc"}]""",
            alias="sortBy",
        ),
    ) -> PaginatedResponse:
        """List groups"""

        params = query_params_parser(
            filters=filters,
            items_per_page=items_per_page,
            page=page,
            search=search,
            sort_by=sort_by,
        )

        return self.model_dto.list(params)

    async def create(self, group: GroupCreate) -> GroupOut:
        """Create group"""

        return self.model_dto.create(group)

    async def patch(self, group_id: UUID, group: GroupPatch) -> GroupOut:
        """Edit group"""

        return self.model_dto.edit_by_id(group_id, group)

    async def delete(self, group_id: UUID) -> None:
        """Delete group"""

        return self.model_dto.delete_by_id(group_id)


GroupRouter(group_router)
