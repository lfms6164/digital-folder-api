from typing import Any, List
from uuid import UUID

from fastapi import HTTPException

from digital_folder.db.models import Ticket
from digital_folder.helpers.db_operations import DbService
from digital_folder.helpers.utils import PaginatedResponse
from digital_folder.packages.Ticket.schemas import (
    TicketCreate,
    TicketOut,
    TicketPatch,
    TicketState,
)
from digital_folder.supabase.storage import SupabaseDTO


class TicketDTO:
    def __init__(self):
        self.db = DbService()
        self.supabase_storage_bucket = "tickets"

    def list(self) -> PaginatedResponse:
        """
        Retrieve all tickets from the database.

        Returns:
            List[TicketOut]: A list of all tickets.
        """

        tickets, count = self.db.get_all(Ticket)
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

        ticket_obj = self.ticket_parser(ticket)

        return ticket_obj

    def create(self, ticket_data: TicketCreate) -> TicketOut:
        """
        Create a new ticket.

        Args:
            ticket_data (TicketCreate): The ticket data.

        Returns:
            TicketOut: The created ticket object.
        """

        ticket = self.db.create(Ticket, ticket_data.dict())

        if ticket.image:
            SupabaseDTO(self.supabase_storage_bucket).move_files(
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

        self.db.update(Ticket, ticket_id, ticket_data.dict(exclude_unset=True))

        return self.get_by_id(ticket_id)

    def delete_by_id(self, ticket_id: UUID) -> None:
        """
        Delete a ticket by its ID.

        Args:
            ticket_id (UUID): The ticket ID.
        """

        ticket = self.get_by_id(ticket_id)
        if ticket.image:
            SupabaseDTO(self.supabase_storage_bucket).delete_folder(str(ticket_id))

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
            "state": TicketState(ticket.state.value),
            "created_at": ticket.created_at,
            "updated_at": ticket.updated_at or None,
        }

        return TicketOut(
            id=parsed_ticket["id"],
            name=parsed_ticket["name"],
            description=parsed_ticket["description"],
            image=parsed_ticket["image"],
            state=parsed_ticket["state"],
            created_at=parsed_ticket["created_at"],
            updated_at=parsed_ticket["updated_at"],
        )
