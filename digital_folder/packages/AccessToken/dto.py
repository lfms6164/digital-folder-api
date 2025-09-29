from datetime import timedelta, datetime

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from digital_folder.core.config import project_settings
from digital_folder.packages.AccessToken.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


def create_access_token(token_data: TokenData) -> str:
    expire = datetime.now() + timedelta(
        minutes=project_settings.access_token_expires_in
    )

    to_encode = {"id": token_data.id, "exp": expire}

    encoded_jwt = jwt.encode(
        to_encode,
        project_settings.jwt_secret_key.get_secret_value(),
        algorithm=project_settings.jwt_algorithm,
    )

    return str(encoded_jwt)
