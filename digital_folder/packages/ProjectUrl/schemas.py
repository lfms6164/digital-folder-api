from typing import Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl

from digital_folder.helpers.utils import create_schema_with_exclusions


class ProjectUrlBase(BaseModel):
    """Project Url Base schema"""

    id: UUID
    name: Optional[str] = None
    url: HttpUrl


ProjectUrlCreate = create_schema_with_exclusions(
    schema_name="ProjectUrlCreate",
    base_schema=ProjectUrlBase,
    excluding_fields=["id"],
)

ProjectUrlPatch = create_schema_with_exclusions(
    schema_name="ProjectUrlPatch",
    base_schema=ProjectUrlCreate,
    excluding_fields=[],
    optional=True,
)

ProjectUrlOut = create_schema_with_exclusions(
    schema_name="ProjectUrlOut",
    base_schema=ProjectUrlBase,
    excluding_fields=[],
)
