from typing import Optional, Union
from uuid import UUID

from fastapi import HTTPException

from digital_folder.core.auth import validate_ownership, validate_unique
from digital_folder.core.pagination.types import PaginatedResponse, QueryParams
from digital_folder.db.models import Tag
from digital_folder.db.service import DbService
from digital_folder.packages.Group.dto import GroupDTO
from digital_folder.packages.Tag.schemas import (
    TagCreate,
    TagPatch,
    TagOut,
    TagWithoutGroupOut,
)


class TagDTO:
    def __init__(self, db: DbService):
        self.db = db

    def list(self, params: QueryParams) -> PaginatedResponse:
        """
        Retrieve tags from the database.

        Args:
            params (QueryParams): Params to select what data to retrieve.
            Can include filters, items per page, page, search and sort by.

        Returns:
            PaginatedResponse: Contains a list of tags and the count.
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

        return self.tag_parser(tag)

    def create(self, tag_data: TagCreate) -> TagOut:
        """
        Create a new tag.

        Args:
            tag_data (TagCreate): The tag data.

        Returns:
            TagOut: The created tag data.
        """

        validate_ownership(GroupDTO(self.db), [tag_data.group_id], True)
        validate_unique(self.db, Tag, tag_data.name)

        tag_dict = tag_data.dict()
        tag_dict["created_by"] = self.db.user.id
        tag_obj = self.db.create(Tag, tag_dict)

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

        validate_ownership(self, [tag_id])
        if tag_data.group_id:
            validate_ownership(GroupDTO(self.db), [tag_data.group_id], True)
        if tag_data.name:
            validate_unique(self.db, Tag, tag_data.name)

        self.db.update(Tag, tag_id, tag_data.dict(exclude_unset=True))

        return self.get_by_id(tag_id)

    def delete_by_id(self, tag_id: UUID) -> None:
        """
        Delete a tag by its ID. Relations are deleted automatically.

        Args:
            tag_id (UUID): The tag ID.
        """

        validate_ownership(self, [tag_id])

        self.db.delete(Tag, tag_id)

    def tag_parser(
        self, tag: Tag, include_group: Optional[bool] = True
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
                "group": GroupDTO(self.db).group_parser(tag.group, False),
                "group_id": tag.group_id,
                "created_by": tag.created_by,
            }

            return TagOut(
                id=parsed_tag["id"],
                name=parsed_tag["name"],
                icon=parsed_tag["icon"],
                color=parsed_tag["color"],
                group=parsed_tag["group"],
                group_id=parsed_tag["group_id"],
                created_by=parsed_tag["created_by"],
            )

        parsed_tag = {
            "id": tag.id,
            "name": tag.name or None,
            "icon": tag.icon or None,
            "color": tag.color,
            "created_by": tag.created_by,
        }

        return TagWithoutGroupOut(
            id=parsed_tag["id"],
            name=parsed_tag["name"],
            icon=parsed_tag["icon"],
            color=parsed_tag["color"],
            created_by=parsed_tag["created_by"],
        )
