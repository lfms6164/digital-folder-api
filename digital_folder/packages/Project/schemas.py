from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from digital_folder.helpers.schema_utils import create_schema_with_exclusions
from digital_folder.packages.Tag.schemas import TagOut


class ProjectBase(BaseModel):
    """Project Base schema"""

    id: UUID
    name: str
    image: Optional[str] = None
    introduction: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[TagOut]] = None


ProjectCreate = create_schema_with_exclusions(
    schema_name="ProjectCreate",
    base_schema=ProjectBase,
    excluding_fields=["id"],
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
