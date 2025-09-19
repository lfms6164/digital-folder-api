from typing import Any, List, Optional, Union
from uuid import UUID

from fastapi import HTTPException

from digital_folder.db.models import Tag
from digital_folder.helpers.db_operations import DbService
from digital_folder.helpers.utils import QueryParams, PaginatedResponse
from digital_folder.packages.Group.dto import GroupDTO
from digital_folder.packages.Tag.schemas import (
    TagCreate,
    TagOut,
    TagPatch,
    TagWithoutGroupOut,
)


class TagDTO:
    def __init__(self):
        self.db = DbService()

    def list(self, params: QueryParams) -> PaginatedResponse:
        """
        Retrieve all tags from the database.

        Returns:
            List[TagOut]: A list of all tags.
        """

        tags, count = self.db.get_all(Tag, params)
        parsed_tags = []
        for tag in tags:
            tag = self.tag_parser(tag)
            parsed_tags.append(tag)

        return PaginatedResponse(items=parsed_tags, count=count)

    def get_by_id(self, tag_id: UUID) -> TagOut:
        """
        Retrieve a tag by its ID.

        Args:
            tag_id (UUID): The tag ID.

        Returns:
            TagOut: The tag data.
        """

        tag = self.db.get_by_id(Tag, tag_id)
        if not tag:
            raise HTTPException(status_code=400, detail=f"Tag {tag_id} not found.")

        tag_obj = self.tag_parser(tag)

        return tag_obj

    def create(self, tag: TagCreate) -> TagOut:
        """
        Create a new tag.

        Args:
            tag (TagCreate): The tag data.

        Returns:
            TagOut: The created tag data.
        """

        tag_obj = self.db.create(Tag, tag.dict())

        return self.tag_parser(tag_obj)

    def edit_by_id(self, tag_id: UUID, tag_data: TagPatch) -> TagOut:
        """
        Edit a tag by its ID.

        Args:
            tag_id (UUID): The tag ID.
            tag_data (TagPatch): The tag data.

        Returns:
            TagOut: The patched tag data.
        """

        self.db.update(Tag, tag_id, tag_data.dict(exclude_unset=True))

        return self.get_by_id(tag_id)

    def delete_by_id(self, tag_id: UUID) -> None:
        """
        Delete a tag by its ID. Relations are deleted automatically.

        Args:
            tag_id (UUID): The tag ID.
        """

        self.db.delete(Tag, tag_id)

    @staticmethod
    def tag_parser(
        tag: Any, include_group: Optional[bool] = True
    ) -> Union[TagOut, TagWithoutGroupOut]:
        """
        This function takes tag data and turns it into a TagOut object.

        Args:
            tag (Any): The tag data.
            include_group (Optional[bool]): Flag to return tag with or without group.

        Returns:
            TagOut: The parsed tag data.
        """

        if include_group:
            parsed_tag = {
                "id": tag.id,
                "name": tag.name or None,
                "icon": tag.icon or None,
                "color": tag.color,
                "group": GroupDTO().group_parser(tag.group, False),
                "group_id": tag.group_id,
            }

            return TagOut(
                id=parsed_tag["id"],
                name=parsed_tag["name"],
                icon=parsed_tag["icon"],
                color=parsed_tag["color"],
                group=parsed_tag["group"],
                group_id=parsed_tag["group_id"],
            )

        parsed_tag = {
            "id": tag.id,
            "name": tag.name or None,
            "icon": tag.icon or None,
            "color": tag.color,
        }

        return TagWithoutGroupOut(
            id=parsed_tag["id"],
            name=parsed_tag["name"],
            icon=parsed_tag["icon"],
            color=parsed_tag["color"],
        )
