from uuid import UUID

from fastapi import HTTPException

from digital_folder.core.config import project_settings
from digital_folder.db.models import User
from digital_folder.db.service import DbService
from digital_folder.helpers.secrets import verify_password
from digital_folder.packages.AccessToken.dto import create_access_token
from digital_folder.packages.AccessToken.schemas import TokenData
from digital_folder.packages.User.schemas import (
    UserLoginForm,
    UserLoginResponse,
    UserRole,
    UserOut,
)


class UserDTO:
    def __init__(self, db: DbService):
        self.db = db

    def login(self, form_data: UserLoginForm) -> UserLoginResponse:
        """
        Authenticate a user using their credentials and generate a JWT access token.
        Starts by checking if user exists in the database, then validates password,
        then creates an access token and returns the UserLoginResponse.

        Args:
            form_data (UserLoginForm): The login form data containing the username and password.

        Returns:
            UserLoginResponse: Contains the JWT access token, its type and the authenticated user.
        """

        user = self.db.get_by_field(User, form_data.username, "username")
        if not user:
            raise HTTPException(
                status_code=400,
                detail=f"User {form_data.username} not found.",
            )

        if not verify_password(form_data.password.get_secret_value(), user.password):
            raise HTTPException(
                status_code=400,
                detail="Login failed - Invalid username or password.",
            )

        token_data = TokenData(id=str(user.id))
        access_token = create_access_token(token_data)

        parsed_user = self.user_parser(user)

        return UserLoginResponse(
            access_token=access_token, token_type="bearer", user=parsed_user
        )

    def get_by_id(self, user_id: UUID) -> UserOut:
        """
        Retrieve a user by its ID.

        Args:
            user_id (UUID): The user ID.

        Returns:
            UserOut: The user data.
        """

        user = self.db.get_by_id(User, user_id)
        if not user:
            raise HTTPException(status_code=400, detail=f"User {user_id} not found.")

        return self.user_parser(user)

    def get_by_field(self, value: str, column_name: str) -> UserOut:
        """
        Retrieve a user by any user field.

        Args:
            value (str): The value to get the user.
            column_name (str): The column to search the value from.

        Returns:
            UserOut: The user data.
        """

        user = self.db.get_by_field(User, value, column_name)
        if not user:
            raise HTTPException(
                status_code=400,
                detail=f"User: { {column_name: value} } not found.",
            )

        return self.user_parser(user)

    @staticmethod
    def user_parser(user: User) -> UserOut:
        """
        This function takes user data and turns it into a UserOut object.

        Args:
            user (Any): The user data.

        Returns:
            UserOut: The parsed user data.
        """

        return UserOut(
            id=user.id,
            username=user.username,
            env=project_settings.env.lower(),
            role=UserRole(user.role.value),
        )
