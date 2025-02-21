"""Core settings"""

from typing import List

from pydantic import MySQLDsn, HttpUrl, SecretStr

from digital_folder import __version__
from digital_folder.helpers.helper_methods import get_scrt_key
from pydantic.v1 import BaseSettings, AnyHttpUrl


class ProjectSettingsBase(BaseSettings):
    """Project Settings Base"""

    # backend_cors_origins: List[AnyHttpUrl] = [HttpUrl("http://localhost:5173")]
    backend_cors_origins: str = "http://localhost:5173"


class ProjectSettings(ProjectSettingsBase):
    """Project settings"""

    project_name: str = "DigitalFolder"
    project_version: str = __version__

    mysql_uri: MySQLDsn = MySQLDsn("mysql+pymysql://root:pswrd@localhost")
    EXCEL_DB_PATH = r"C:\Users\Player One\repos\DigitalFolder\digitalfolder_db.xlsx"

    jwt_secret_key: SecretStr = get_scrt_key(EXCEL_DB_PATH)
    jwt_algorithm: str = "HS256"

    access_token_expires_in: int = 30


project_settings = ProjectSettings()
