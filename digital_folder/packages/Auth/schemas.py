from pydantic import BaseModel, SecretStr


class AuthBase(BaseModel):
    """Auth Base schema"""

    username: str
    password: SecretStr
