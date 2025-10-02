from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from digital_folder.helpers.utils import create_schema_with_exclusions


class TicketStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class TicketBase(BaseModel):
    """Ticket Base schema"""

    id: UUID
    name: str
    description: str
    image: Optional[str] = None
    status: TicketStatus
    created_by: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None


TicketCreate = create_schema_with_exclusions(
    schema_name="TicketCreate",
    base_schema=TicketBase,
    excluding_fields=["id", "status", "created_by", "created_at", "updated_at"],
)

TicketPatch = create_schema_with_exclusions(
    schema_name="TicketPatch",
    base_schema=TicketBase,
    excluding_fields=[
        "id",
        "name",
        "description",
        "image",
        "created_by",
        "created_at",
        "updated_at",
    ],
    optional=True,
)

TicketOut = create_schema_with_exclusions(
    schema_name="TicketOut",
    base_schema=TicketBase,
    excluding_fields=[],
)
