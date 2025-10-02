from typing import Any, List
from uuid import UUID

from fastapi import HTTPException

from digital_folder.core.auth import validate_ownership, validate_unique
from digital_folder.core.pagination import PaginatedResponse, QueryParams
from digital_folder.db.models import Ticket
from digital_folder.db.service import DbService
from digital_folder.packages.Ticket.schemas import (
    TicketCreate,
    TicketPatch,
    TicketOut,
    TicketStatus,
)
from digital_folder.supabase.client import SupabaseStorageConfig
from digital_folder.supabase.storage import SupabaseDTO


class TicketDTO:
    def __init__(self, db: DbService):
        self.db = db
        self.supabase_storage_config = SupabaseStorageConfig(
            bucket=self.db.user.env, folder="tickets"
        )

    def list(self, params: QueryParams) -> PaginatedResponse:
        """
        Retrieve all tickets from the database.

        Returns:
            List[TicketOut]: A list of all tickets.
        """

        tickets, count = self.db.get_all(Ticket, params)
        parsed_tickets = []
        for ticket in tickets:
            ticket = self.ticket_parser(ticket)
            parsed_tickets.append(ticket)

        return PaginatedResponse(items=parsed_tickets, count=count)

    def get_by_id(self, ticket_id: UUID) -> TicketOut:
        """
        Retrieve a ticket by its ID.

        Args:
            ticket_id (UUID): The ticket ID.

        Returns:
            TicketOut: The ticket object.
        """

        ticket = self.db.get_by_id(Ticket, ticket_id)
        if not ticket:
            raise HTTPException(
                status_code=400, detail=f"Ticket {ticket_id} not found."
            )

        return self.ticket_parser(ticket)

    def create(self, ticket_data: TicketCreate) -> TicketOut:
        """
        Create a new ticket.

        Args:
            ticket_data (TicketCreate): The ticket data.

        Returns:
            TicketOut: The created ticket object.
        """

        validate_unique(self.db, Ticket, ticket_data.name)

        ticket_dict = ticket_data.dict()
        ticket_dict["created_by"] = self.db.user.id
        ticket = self.db.create(Ticket, ticket_dict)

        if ticket.image:
            SupabaseDTO(self.supabase_storage_config).move_files(
                [ticket.image], str(ticket.id)
            )

        return self.ticket_parser(ticket)

    def edit_by_id(self, ticket_id: UUID, ticket_data: TicketPatch) -> TicketOut:
        """
        Edit a ticket by its ID.

        Args:
            ticket_id (UUID): The ticket ID.
            ticket_data (TicketPatch): The ticket data.

        Returns:
            TicketOut: The patched ticket object.
        """

        validate_ownership(self, [ticket_id])

        self.db.update(Ticket, ticket_id, ticket_data.dict(exclude_unset=True))

        return self.get_by_id(ticket_id)

    def delete_by_id(self, ticket_id: UUID) -> None:
        """
        Delete a ticket by its ID.

        Args:
            ticket_id (UUID): The ticket ID.
        """

        validate_ownership(self, [ticket_id])

        ticket = self.get_by_id(ticket_id)
        if ticket.image:
            SupabaseDTO(self.supabase_storage_config).delete_folder(str(ticket_id))

        self.db.delete(Ticket, ticket_id)

    @staticmethod
    def ticket_parser(ticket: Any) -> TicketOut:
        """
        This function takes ticket data and turns it into a TicketOut object.

        Args:
            ticket (Any): The ticket data.

        Returns:
            GroupOut: The parsed ticket object.
        """

        parsed_ticket = {
            "id": ticket.id,
            "name": ticket.name,
            "description": ticket.description,
            "image": ticket.image or None,
            "status": TicketStatus(ticket.status.value),
            "created_by": ticket.created_by,
            "created_at": ticket.created_at,
            "updated_at": ticket.updated_at or None,
        }

        return TicketOut(
            id=parsed_ticket["id"],
            name=parsed_ticket["name"],
            description=parsed_ticket["description"],
            image=parsed_ticket["image"],
            status=parsed_ticket["status"],
            created_by=parsed_ticket["created_by"],
            created_at=parsed_ticket["created_at"],
            updated_at=parsed_ticket["updated_at"],
        )
