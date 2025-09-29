from pydantic import BaseModel


class TokenData(BaseModel):
    """Token Data schema"""

    id: str


class Token(BaseModel):
    """Token schema"""

    access_token: str
    token_type: str
