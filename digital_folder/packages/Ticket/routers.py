from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from digital_folder.core.dependencies import get_db_validate_role, get_db_validate_user
from digital_folder.core.pagination.types import PaginatedResponse
from digital_folder.core.pagination.utils import query_params_parser
from digital_folder.db.service import DbService
from digital_folder.packages.Ticket.dto import TicketDTO
from digital_folder.packages.Ticket.schemas import TicketCreate, TicketPatch, TicketOut

ticket_router = APIRouter()


class TicketRouter:
    def __init__(self, router: APIRouter):
        self.model_dto = TicketDTO
        self.router = router
        self.router.add_api_route("/list", self.list, methods=["GET"])
        self.router.add_api_route("/create", self.create, methods=["POST"])
        self.router.add_api_route("/patch/{ticket_id}", self.patch, methods=["PATCH"])
        self.router.add_api_route(
            "/delete/{ticket_id}", self.delete, methods=["DELETE"]
        )

    async def list(
        self,
        filters: Optional[str] = Query(
            None, description="""User UUID ex: {"created_by":{id}}"""
        ),
        db: DbService = Depends(get_db_validate_user),
    ) -> PaginatedResponse:
        """List tickets"""

        params = query_params_parser(
            db=db,
            filters=filters,
        )

        return self.model_dto(db).list(params)

    async def create(
        self,
        ticket: TicketCreate,
        db: DbService = Depends(get_db_validate_user),
    ) -> TicketOut:
        """Create ticket"""

        return self.model_dto(db).create(ticket)

    async def patch(
        self,
        ticket_id: UUID,
        ticket: TicketPatch,
        db: DbService = Depends(get_db_validate_role),
    ) -> TicketOut:
        """Edit ticket"""

        return self.model_dto(db).edit_by_id(ticket_id, ticket)

    async def delete(
        self, ticket_id: UUID, db: DbService = Depends(get_db_validate_role)
    ) -> None:
        """Delete ticket"""

        return self.model_dto(db).delete_by_id(ticket_id)


TicketRouter(ticket_router)
