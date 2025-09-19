from uuid import UUID

from fastapi import APIRouter

from digital_folder.helpers.utils import PaginatedResponse
from digital_folder.packages.Ticket.dto import TicketDTO
from digital_folder.packages.Ticket.schemas import TicketCreate, TicketOut, TicketPatch

ticket_router = APIRouter()


class TicketRouter:
    def __init__(self, router: APIRouter):
        self.model_dto = TicketDTO()
        self.router = router
        self.router.add_api_route("/list", self.list, methods=["GET"])
        self.router.add_api_route("/create", self.create, methods=["POST"])
        self.router.add_api_route("/patch/{ticket_id}", self.patch, methods=["PATCH"])
        self.router.add_api_route(
            "/delete/{ticket_id}", self.delete, methods=["DELETE"]
        )

    async def list(self) -> PaginatedResponse:
        """List tickets"""

        return self.model_dto.list()

    async def create(self, ticket: TicketCreate) -> TicketOut:
        """Create ticket"""

        return self.model_dto.create(ticket)

    async def patch(self, ticket_id: UUID, ticket: TicketPatch) -> TicketOut:
        """Edit ticket"""

        return self.model_dto.edit_by_id(ticket_id, ticket)

    async def delete(self, ticket_id: UUID) -> None:
        """Delete ticket"""

        return self.model_dto.delete_by_id(ticket_id)


TicketRouter(ticket_router)
