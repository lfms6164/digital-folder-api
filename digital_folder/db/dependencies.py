from fastapi import Depends

from digital_folder.core.dependencies import validate_role, validate_user
from digital_folder.db.service import DbService


def get_db_validate_user(user=Depends(validate_user)):
    with DbService(user) as db:
        yield db


def get_db_validate_role(user=Depends(validate_role)):
    with DbService(user) as db:
        yield db
