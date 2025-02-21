from uuid import UUID

from pydantic import BaseModel


class RelationBase(BaseModel):
    """Relation Base schema"""

    project_id: UUID
    tag_id: UUID
