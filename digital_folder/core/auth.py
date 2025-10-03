from typing import Any, List, Optional, Type
from uuid import UUID

from fastapi import HTTPException

from digital_folder.db.service import DbService
from digital_folder.db.types import ModelType
from digital_folder.packages.User.schemas import UserRole


def validate_ownership(
    dto: Any, obj_ids: List[UUID], relation: Optional[bool] = False
) -> None:
    """
    Safety check to validate if the user executing an action has ownership over the objects.

    This check is applied in 2 different scenarios, and the 'relation' flag is used to
    alternate between the 2:
        - During CREATE of objects with relations (Project or Tag) to determine if the user
            is trying to create an object with a related object owned by a different user.
        - During UPDATE or DELETE to determine if the user executing the action is the one
            who has ownership over the objects.

    Args:
        dto (Any): The DTO.
        obj_ids (List[UUID]): A list of sometimes multiple but mostly just a single UUID.
        relation (Optional[bool]): Flag to determine if the object being validated is a relation or not.
    """

    current_user = dto.db.user
    if not relation:
        if current_user.role == UserRole.ADMIN:
            return

    for obj_id in obj_ids:
        obj = dto.get_by_id(obj_id)
        if obj.created_by != current_user.id:
            raise HTTPException(
                status_code=403,
                detail=f"User '{current_user.username}' doesn't have ownership over '{obj.name}'.",
            )


def validate_unique(db: DbService, model: Type[ModelType], name: str) -> None:
    """
    Safety check used at CREATE or UPDATE to validate if the object being created or updated has a unique name.

    Args:
        db (DbService): DbService class.
        model (Type[ModelType]): The model of the type of object being validated.
        name (str): The name of the object to be searched in the database.
    """

    item = db.get_by_field(model, name, "name")
    if item:
        raise HTTPException(
            status_code=400,
            detail=f"Failed '{name}' already exists.",
        )
