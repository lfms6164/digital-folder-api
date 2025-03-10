from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from digital_folder.helpers.schema_utils import create_schema_with_exclusions


class TagBase(BaseModel):
    """Tag Base schema"""

    id: UUID
    name: Optional[str] = None
    icon: Optional[str] = None
    color: str


TagCreate = create_schema_with_exclusions(
    schema_name="TagCreate",
    base_schema=TagBase,
    excluding_fields=["id"],
)

TagPatch = create_schema_with_exclusions(
    schema_name="TagPatch",
    base_schema=TagCreate,
    excluding_fields=[],
)

TagOut = create_schema_with_exclusions(
    schema_name="TagOut",
    base_schema=TagBase,
    excluding_fields=[],
)
