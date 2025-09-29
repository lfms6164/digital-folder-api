from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from digital_folder.helpers.utils import create_schema_with_exclusions


class GroupBase(BaseModel):
    """Group Base schema"""

    id: UUID
    name: Optional[str] = None
    has_tags: bool = False
    tags: Optional[List["TagWithoutGroupOut"]] = None
    created_by: UUID


GroupCreate = create_schema_with_exclusions(
    schema_name="GroupCreate",
    base_schema=GroupBase,
    excluding_fields=["id", "has_tags", "tags", "created_by"],
)

GroupPatch = create_schema_with_exclusions(
    schema_name="GroupPatch",
    base_schema=GroupCreate,
    excluding_fields=[],
    optional=True,
)

GroupOut = create_schema_with_exclusions(
    schema_name="GroupOut",
    base_schema=GroupBase,
    excluding_fields=[],
)

GroupWithoutTagsOut = create_schema_with_exclusions(
    schema_name="GroupWithoutTagsOut",
    base_schema=GroupBase,
    excluding_fields=["tags"],
)

from digital_folder.packages.Tag.schemas import TagWithoutGroupOut

GroupOut.model_rebuild()
