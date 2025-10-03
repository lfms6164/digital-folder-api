from enum import Enum
from typing import Optional
from uuid import UUID

from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, SecretStr

from digital_folder.helpers.utils import create_schema_with_exclusions
from digital_folder.packages.AccessToken.schemas import Token


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    VIEWER = "VIEWER"


class UserBase(BaseModel):
    """User Base schema"""

    id: UUID
    username: str
    password: SecretStr
    role: UserRole
    env: str
    filter_id: Optional[UUID] = None


UserDb = create_schema_with_exclusions(
    schema_name="UserDb",
    base_schema=UserBase,
    excluding_fields=["password"],
)


UserOut = create_schema_with_exclusions(
    schema_name="UserOut",
    base_schema=UserBase,
    excluding_fields=["password", "filter_id"],
)


class UserLoginForm(OAuth2PasswordRequestForm):
    def __init__(self, username: str = Form(...), password: SecretStr = Form(...)):
        super().__init__(username=username, password=password.get_secret_value())
        self.password = password


class UserLoginResponse(Token):
    user: UserOut
