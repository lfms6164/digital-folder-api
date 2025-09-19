from typing import Any, List, Optional, Union
from uuid import UUID

from fastapi import HTTPException

from digital_folder.db.models import Group
from digital_folder.helpers.db_operations import DbService
from digital_folder.helpers.utils import QueryParams, PaginatedResponse
from digital_folder.packages.Group.schemas import (
    GroupCreate,
    GroupOut,
    GroupPatch,
    GroupWithoutTagsOut,
)


class GroupDTO:
    def __init__(self):
        self.db = DbService()

    def list(self, params: QueryParams) -> PaginatedResponse:
        """
        Retrieve all groups from the database.

        Returns:
            List[GroupOut]: A list of all groups.
        """

        groups, count = self.db.get_all(Group, params)
        parsed_groups = []
        for group in groups:
            group = self.group_parser(group, True)
            parsed_groups.append(group)

        return PaginatedResponse(items=parsed_groups, count=count)

    def get_by_id(self, group_id: UUID) -> GroupOut:
        """
        Retrieve a group by its ID.

        Args:
            group_id (UUID): The group ID.

        Returns:
            GroupOut: The group object.
        """

        group = self.db.get_by_id(Group, group_id)
        if not group:
            raise HTTPException(status_code=400, detail=f"Group {group_id} not found.")

        group_obj = self.group_parser(group)

        return group_obj

    def create(self, group: GroupCreate) -> GroupOut:
        """
        Create a new group.

        Args:
            group (GroupCreate): The group data.

        Returns:
            GroupOut: The created group object.
        """

        group_obj = self.db.create(Group, group.dict())

        return self.group_parser(group_obj)

    def edit_by_id(self, group_id: UUID, group_data: GroupPatch) -> GroupOut:
        """
        Edit a group by its ID.

        Args:
            group_id (UUID): The group ID.
            group_data (GroupPatch): The group data.

        Returns:
            GroupOut: The patched group object.
        """

        self.db.update(Group, group_id, group_data.dict(exclude_unset=True))

        return self.get_by_id(group_id)

    def delete_by_id(self, group_id: UUID) -> None:
        """
        Delete a group by its ID if it doesn't have relations.

        Args:
            group_id (UUID): The group ID.
        """

        group = self.get_by_id(group_id)
        if group.has_tags:
            raise HTTPException(
                status_code=400,
                detail=f"Group {group.name} has tags and can't be deleted.",
            )

        self.db.delete(Group, group.id)

    @staticmethod
    def group_parser(
        group: Any, include_tags: Optional[bool] = False
    ) -> Union[GroupOut, GroupWithoutTagsOut]:
        """
        This function takes group data and turns it into a GroupOut object.

        Args:
            group (Any): The group data.
            include_tags (Optional[bool]): Flag to return group with or without tags.

        Returns:
            GroupOut: The parsed group object.
        """

        if include_tags:
            from digital_folder.packages.Tag.dto import TagDTO

            tag_dto = TagDTO()

            parsed_group = {
                "id": group.id,
                "name": group.name or None,
                "has_tags": True if group.tags else False,
                "tags": (
                    [tag_dto.tag_parser(tag, False) for tag in group.tags]
                    if group.tags
                    else []
                ),
            }

            return GroupOut(
                id=parsed_group["id"],
                name=parsed_group["name"],
                has_tags=parsed_group["has_tags"],
                tags=parsed_group["tags"],
            )

        parsed_group = {
            "id": group.id,
            "name": group.name or None,
            "has_tags": True if group.tags else False,
        }

        return GroupWithoutTagsOut(
            id=parsed_group["id"],
            name=parsed_group["name"],
            has_tags=parsed_group["has_tags"],
        )
