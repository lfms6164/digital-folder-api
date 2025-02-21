from typing import List

from fastapi import APIRouter

from digital_folder.packages.Tag.dto import TagDTO
from digital_folder.packages.Tag.schemas import TagOut, TagCreate, TagPatch

tag_router = APIRouter()


class TagRouter:

    model_dto = TagDTO

    @staticmethod
    @tag_router.get(path="/list")
    def list() -> List[TagOut]:
        """List tags"""

        return TagDTO.list()

    @staticmethod
    @tag_router.post(path="/create")
    def create(tag: TagCreate) -> TagOut:
        """Create tag"""

        return TagDTO.create(tag)

    @staticmethod
    @tag_router.patch(path="/patch/{tag_id}")
    def patch(tag_id: str, tag: TagPatch) -> TagOut:
        """Edit tag"""

        return TagDTO.edit_by_id(tag_id, tag)

    @staticmethod
    @tag_router.delete(path="/delete/{tag_id}")
    def delete(tag_id: str) -> None:
        """Delete tag"""

        return TagDTO.delete_by_id(tag_id)
