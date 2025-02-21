from pydantic import BaseModel, SecretStr


class AuthArgs(BaseModel):
    """Auth Args schema"""

    username: str
    password: SecretStr
