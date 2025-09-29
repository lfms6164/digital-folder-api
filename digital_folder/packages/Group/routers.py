from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from digital_folder.core.pagination import PaginatedResponse, query_params_parser
from digital_folder.db.dependencies import get_db_with_user
from digital_folder.db.service import DbService
from digital_folder.packages.Group.dto import GroupDTO
from digital_folder.packages.Group.schemas import (
    GroupCreate,
    GroupPatch,
    GroupOut,
)

group_router = APIRouter()


class GroupRouter:
    def __init__(self, router: APIRouter):
        self.model_dto = GroupDTO
        self.router = router
        self.router.add_api_route("/list", self.list, methods=["GET"])
        self.router.add_api_route("/create", self.create, methods=["POST"])
        self.router.add_api_route("/patch/{group_id}", self.patch, methods=["PATCH"])
        self.router.add_api_route("/delete/{group_id}", self.delete, methods=["DELETE"])

    async def list(
        self,
        filters: Optional[str] = Query(
            None, description="""Has tags? ex: {"has_tags":true}"""
        ),
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
        db: DbService = Depends(get_db_with_user),
    ) -> PaginatedResponse:
        """List groups"""

        params = query_params_parser(
            db=db,
            filters=filters,
            items_per_page=items_per_page,
            page=page,
            search=search,
            sort_by=sort_by,
        )

        return self.model_dto(db).list(params)

    async def create(
        self,
        group: GroupCreate,
        db: DbService = Depends(get_db_with_user),
    ) -> GroupOut:
        """Create group"""

        return self.model_dto(db).create(group)

    async def patch(
        self,
        group_id: UUID,
        group: GroupPatch,
        db: DbService = Depends(get_db_with_user),
    ) -> GroupOut:
        """Edit group"""

        return self.model_dto(db).edit_by_id(group_id, group)

    async def delete(
        self,
        group_id: UUID,
        db: DbService = Depends(get_db_with_user),
    ) -> None:
        """Delete group"""

        return self.model_dto(db).delete_by_id(group_id)


GroupRouter(group_router)
