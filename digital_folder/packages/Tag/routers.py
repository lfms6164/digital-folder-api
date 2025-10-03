from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from digital_folder.core.dependencies import get_db_validate_role, get_db_validate_user
from digital_folder.core.pagination.types import PaginatedResponse
from digital_folder.core.pagination.utils import query_params_parser
from digital_folder.db.service import DbService
from digital_folder.packages.Tag.dto import TagDTO
from digital_folder.packages.Tag.schemas import TagCreate, TagPatch, TagOut

tag_router = APIRouter()


class TagRouter:
    def __init__(self, router: APIRouter):
        self.model_dto = TagDTO
        self.router = router
        self.router.add_api_route("/list", self.list, methods=["GET"])
        self.router.add_api_route("/create", self.create, methods=["POST"])
        self.router.add_api_route("/patch/{tag_id}", self.patch, methods=["PATCH"])
        self.router.add_api_route("/delete/{tag_id}", self.delete, methods=["DELETE"])

    async def list(
        self,
        filters: Optional[str] = Query(None, description="Comma-separated group IDs"),
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
        db: DbService = Depends(get_db_validate_user),
    ) -> PaginatedResponse:
        """List tags"""

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
        tag: TagCreate,
        db: DbService = Depends(get_db_validate_role),
    ) -> TagOut:
        """Create tag"""

        return self.model_dto(db).create(tag)

    async def patch(
        self,
        tag_id: UUID,
        tag: TagPatch,
        db: DbService = Depends(get_db_validate_role),
    ) -> TagOut:
        """Edit tag"""

        return self.model_dto(db).edit_by_id(tag_id, tag)

    async def delete(
        self, tag_id: UUID, db: DbService = Depends(get_db_validate_role)
    ) -> None:
        """Delete tag"""

        return self.model_dto(db).delete_by_id(tag_id)


TagRouter(tag_router)
