"""Core settings"""

import os
from typing import List, Optional

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))


class ProjectSettingsBase(BaseSettings):
    """Project Settings Base"""

    # CORS
    backend_cors_origins: List[str]


class ProjectSettings(ProjectSettingsBase):
    """Project settings"""

    # App
    project_name: str
    project_version: str
    debug: Optional[bool] = False
    env: str
    port: Optional[int] = None

    # Database
    dev_database_url: Optional[str] = None
    prod_database_url: str

    # JWT
    jwt_secret_key: SecretStr
    jwt_algorithm: str
    access_token_expires_in: int

    # Supabase
    project_url: str
    public_key: str
    service_role_key: str

    model_config = SettingsConfigDict(env_file=DOTENV, env_file_encoding="utf-8")


project_settings = ProjectSettings()
