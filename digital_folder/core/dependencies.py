from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from digital_folder.core.config import project_settings
from digital_folder.db.db import get_db
from digital_folder.db.service import DbService
from digital_folder.packages.User.dto import UserDTO
from digital_folder.packages.User.schemas import (
    UserDb,
    UserRole,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


def validate_user(
    db: DbService = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> UserDb:
    """
    Validate and decode the JWT access token, then return the authenticated user.
    This dependency is used to protect routes that require authentication.

    Args:
        db (DbService): The database service dependency.
        token (str): The JWT access token extracted from the Authorization header.

    Returns:
        UserDb: The authenticated user, including role and environment data.
    """

    try:
        payload = jwt.decode(
            token,
            project_settings.jwt_secret_key.get_secret_value(),
            algorithms=[project_settings.jwt_algorithm],
        )

        user_id = UUID(payload.get("id"))
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid access token.",
            )

    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="JWTError")

    user = UserDTO(db).get_by_id(user_id)

    role_config = {
        UserRole.ADMIN: None,
        UserRole.USER: user.id,
        UserRole.VIEWER: UserDTO(db).get_by_field(UserRole.ADMIN, "role").id,
    }

    return UserDb(
        id=user.id,
        username=user.username,
        role=user.role,
        env=project_settings.env.lower(),
        filter_id=role_config[user.role],
    )


def validate_role(user: UserDb = Depends(validate_user)) -> UserDb:
    """
    Protect some actions by checking if user has write permissions based on its role.

    Args:
        user (UserDb): The authenticated user returned by 'validate_user'.

    Returns:
        UserDb: The user if passes role check.
    """

    if user.role not in [UserRole.ADMIN, UserRole.USER]:
        raise HTTPException(
            status_code=403,
            detail=f"User '{user.username}' does not have permission to perform this action.",
        )
    return user
