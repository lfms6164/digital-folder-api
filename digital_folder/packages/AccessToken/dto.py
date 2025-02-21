from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from digital_folder.core.config import project_settings
from digital_folder.packages.AccessToken.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth")


class AccessTokenDTO:
    @staticmethod
    def create_access_token(token_data: TokenData) -> str:
        expire = datetime.now() + timedelta(minutes=15)

        to_encode = {"username": token_data.username, "exp": expire}

        encoded_jwt = jwt.encode(
            to_encode,
            project_settings.jwt_secret_key.get_secret_value(),
            algorithm=project_settings.jwt_algorithm,
        )

        return str(encoded_jwt)

    @staticmethod
    def get_token_data(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(
                token,
                project_settings.jwt_secret_key.get_secret_value(),
                algorithms=[project_settings.jwt_algorithm],
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="JWTError"
            )

        return payload
