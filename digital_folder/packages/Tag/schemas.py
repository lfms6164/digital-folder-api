from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from digital_folder.helpers.utils import create_schema_with_exclusions
from digital_folder.packages.Group.schemas import GroupWithoutTagsOut


class TagBase(BaseModel):
    """Tag Base schema"""

    id: UUID
    name: str
    icon: Optional[str] = None
    color: str
    group: GroupWithoutTagsOut
    group_id: UUID


TagCreate = create_schema_with_exclusions(
    schema_name="TagCreate",
    base_schema=TagBase,
    excluding_fields=["id", "group"],
)

TagPatch = create_schema_with_exclusions(
    schema_name="TagPatch",
    base_schema=TagCreate,
    excluding_fields=[],
    optional=True,
)

TagOut = create_schema_with_exclusions(
    schema_name="TagOut",
    base_schema=TagBase,
    excluding_fields=[],
)

TagWithoutGroupOut = create_schema_with_exclusions(
    schema_name="TagWithoutGroupOut",
    base_schema=TagBase,
    excluding_fields=["group", "group_id"],
)
