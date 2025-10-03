from typing import Optional, Union
from uuid import UUID

from fastapi import HTTPException

from digital_folder.core.auth import validate_ownership, validate_unique
from digital_folder.core.pagination import PaginatedResponse, QueryParams
from digital_folder.db.models import Group
from digital_folder.db.service import DbService
from digital_folder.packages.Group.schemas import (
    GroupCreate,
    GroupPatch,
    GroupOut,
    GroupWithoutTagsOut,
)


class GroupDTO:
    def __init__(self, db: DbService):
        self.db = db

    def list(self, params: QueryParams) -> PaginatedResponse:
        """
        Retrieve groups from the database.

        Args:
            params (QueryParams): Params to select what data to retrieve.
            Can include filters, items per page, page, search and sort by.

        Returns:
            PaginatedResponse: Contains a list of groups and the count.
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

        return self.group_parser(group)

    def create(self, group_data: GroupCreate) -> GroupOut:
        """
        Create a new group.

        Args:
            group_data (GroupCreate): The group data.

        Returns:
            GroupOut: The created group object.
        """

        validate_unique(self.db, Group, group_data.name)

        group_dict = group_data.dict()
        group_dict["created_by"] = self.db.user.id
        group_obj = self.db.create(Group, group_dict)

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

        validate_ownership(self, [group_id])
        if group_data.name:
            validate_unique(self.db, Group, group_data.name)

        self.db.update(Group, group_id, group_data.dict(exclude_unset=True))

        return self.get_by_id(group_id)

    def delete_by_id(self, group_id: UUID) -> None:
        """
        Delete a group by its ID if it doesn't have relations.

        Args:
            group_id (UUID): The group ID.
        """

        validate_ownership(self, [group_id])

        group = self.get_by_id(group_id)
        if group.has_tags:
            raise HTTPException(
                status_code=400,
                detail=f"Group {group.name} has tags and can't be deleted.",
            )

        self.db.delete(Group, group.id)

    def group_parser(
        self, group: Group, include_tags: Optional[bool] = False
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

            tag_dto = TagDTO(self.db)

            parsed_group = {
                "id": group.id,
                "name": group.name or None,
                "has_tags": True if group.tags else False,
                "tags": (
                    [tag_dto.tag_parser(tag, False) for tag in group.tags]
                    if group.tags
                    else []
                ),
                "created_by": group.created_by,
            }

            return GroupOut(
                id=parsed_group["id"],
                name=parsed_group["name"],
                has_tags=parsed_group["has_tags"],
                tags=parsed_group["tags"],
                created_by=parsed_group["created_by"],
            )

        parsed_group = {
            "id": group.id,
            "name": group.name or None,
            "has_tags": True if group.tags else False,
            "created_by": group.created_by,
        }

        return GroupWithoutTagsOut(
            id=parsed_group["id"],
            name=parsed_group["name"],
            has_tags=parsed_group["has_tags"],
            created_by=parsed_group["created_by"],
        )
