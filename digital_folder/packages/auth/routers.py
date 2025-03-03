from http.client import HTTPException
from typing import Any
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status

from digital_folder.core.config import project_settings
from digital_folder.packages.AccessToken.dto import AccessTokenDTO
from digital_folder.packages.AccessToken.schemas import Token, TokenData
from digital_folder.packages.auth.schemas import AuthArgs

auth_router = APIRouter()


class AuthRouter:

    model_dto = AccessTokenDTO

    @staticmethod
    @auth_router.post("/login")
    def login(credential: AuthArgs) -> Any:
        if (
            credential.password.get_secret_value()
            == project_settings.jwt_secret_key.get_secret_value()
        ):
            token_data = TokenData(username=credential.username)
            token = AccessTokenDTO.create_access_token(token_data)
            return Token(access_token=token, token_type="bearer")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Login failed - Invalid credentials",
            )

    @staticmethod
    @auth_router.post("/generate_random_uuid")
    def random_uuid() -> UUID:
        return uuid4()
