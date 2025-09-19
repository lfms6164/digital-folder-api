"""Core settings"""

import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectSettingsBase(BaseSettings):
    """Project Settings Base"""

    # backend_cors_origins: List[AnyHttpUrl] = [HttpUrl("http://localhost:5173")]
    backend_cors_origins: str = "http://localhost:5173"


DOTENV = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))


class ProjectSettings(ProjectSettingsBase):
    """Project settings"""

    project_name: str
    project_version: str
    debug: bool
    env: str

    # mysql_uri: MySQLDsn = MySQLDsn("mysql+pymysql://root:pswrd@localhost")
    dev_database_url: str
    prod_database_url: str

    jwt_secret_key: SecretStr
    jwt_algorithm: str
    access_token_expires_in: int

    project_url: str
    public_key: str
    service_role_key: str

    model_config = SettingsConfigDict(env_file=DOTENV, env_file_encoding="utf-8")


project_settings = ProjectSettings()
