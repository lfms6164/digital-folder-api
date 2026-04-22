from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel

from digital_folder.helpers.utils import create_schema_with_exclusions
from digital_folder.packages.ProjectUrl.schemas import (
    ProjectUrlCreate,
    ProjectUrlPatch,
    ProjectUrlOut,
)
from digital_folder.packages.Tag.schemas import TagOut

UrlType = TypeVar("UrlType")


class ProjectBase(BaseModel, Generic[UrlType]):
    """Project Base schema"""

    id: UUID
    name: str
    urls: Optional[List[UrlType]] = None
    introduction: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[TagOut]] = None
    tag_ids: Optional[List[UUID]] = None
    images: Optional[List[str]] = None
    created_by: UUID


ProjectBaseCreate = ProjectBase[ProjectUrlCreate]
ProjectBasePatch = ProjectBase[ProjectUrlPatch]
ProjectBaseOut = ProjectBase[ProjectUrlOut]


ProjectCreate = create_schema_with_exclusions(
    schema_name="ProjectCreate",
    base_schema=ProjectBaseCreate,
    excluding_fields=["id", "tags", "created_by"],
)

ProjectPatch = create_schema_with_exclusions(
    schema_name="ProjectPatch",
    base_schema=ProjectBasePatch,
    excluding_fields=[],
    optional=True,
)

ProjectOut = create_schema_with_exclusions(
    schema_name="ProjectOut",
    base_schema=ProjectBaseOut,
    excluding_fields=[],
)
