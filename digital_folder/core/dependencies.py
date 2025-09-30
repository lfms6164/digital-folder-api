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
    UserOut,
    UserRole,
    UserRoleConfig,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


def validate_user(
    db: DbService = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> UUID:
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
    env = project_settings.env.lower()

    role_config = {
        UserRole.ADMIN: UserRoleConfig(
            filter_id=None, storage_bucket=env, storage_folder="admin"
        ),
        UserRole.USER: UserRoleConfig(
            filter_id=user.id, storage_bucket=env, storage_folder="user"
        ),
        UserRole.VIEWER: UserRoleConfig(
            filter_id=UserDTO(db).get_by_field(UserRole.ADMIN, "role").id,
            storage_bucket=env,
            storage_folder="admin",
        ),
    }

    return UserDb(
        id=user.id,
        username=user.username,
        role=user.role,
        role_config=role_config[user.role],
    )


def validate_role(user: UserOut = Depends(validate_user)) -> UserOut:
    if user.role not in [UserRole.ADMIN, UserRole.USER]:
        raise HTTPException(
            status_code=403,
            detail=f"User {user.id} does not have permission to perform this action.",
        )
    return user
