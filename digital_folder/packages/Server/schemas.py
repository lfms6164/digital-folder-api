from enum import Enum

from pydantic import BaseModel

from digital_folder.helpers.utils import create_schema_with_exclusions


class ServerStatus(str, Enum):
    ON = "ON"
    IDLE = "IDLE"


class ServerBase(BaseModel):
    """Server Base schema"""

    status: ServerStatus


ServerResponse = create_schema_with_exclusions(
    schema_name="ServerResponse",
    base_schema=ServerBase,
    excluding_fields=[],
)
