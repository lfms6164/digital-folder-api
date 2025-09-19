from http.client import HTTPException
from typing import Any
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from digital_folder.db.db import get_db
from digital_folder.db.models import Auth
from digital_folder.helpers.secrets import verify_password
from digital_folder.packages.AccessToken.dto import AccessTokenDTO
from digital_folder.packages.AccessToken.schemas import Token, TokenData
from digital_folder.packages.Auth.schemas import AuthBase

auth_router = APIRouter()


@auth_router.post("/login")
def login(credentials: AuthBase, db: Session = Depends(get_db)) -> Any:

    user = db.query(Auth).filter_by(username=credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Login failed - User {credentials.username} not in database.",
        )

    if not verify_password(credentials.password.get_secret_value(), user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login failed - Invalid username or password.",
        )

    token_data = TokenData(username=user.username)
    token = AccessTokenDTO.create_access_token(token_data)
    return Token(access_token=token, token_type="bearer")


@auth_router.post("/generate_random_uuid")
def random_uuid() -> UUID:
    return uuid4()
