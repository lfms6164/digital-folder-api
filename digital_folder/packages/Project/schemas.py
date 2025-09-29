from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, HttpUrl

from digital_folder.helpers.utils import create_schema_with_exclusions
from digital_folder.packages.Tag.schemas import TagOut


class ProjectBase(BaseModel):
    """Project Base schema"""

    id: UUID
    name: str
    repo_url: Optional[HttpUrl] = None
    introduction: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[TagOut]] = None
    tag_ids: Optional[List[UUID]] = None
    images: Optional[List[str]] = None
    created_by: UUID


ProjectCreate = create_schema_with_exclusions(
    schema_name="ProjectCreate",
    base_schema=ProjectBase,
    excluding_fields=["id", "tags", "created_by"],
)

ProjectPatch = create_schema_with_exclusions(
    schema_name="ProjectPatch",
    base_schema=ProjectCreate,
    excluding_fields=[],
    optional=True,
)

ProjectOut = create_schema_with_exclusions(
    schema_name="ProjectOut",
    base_schema=ProjectBase,
    excluding_fields=[],
)
