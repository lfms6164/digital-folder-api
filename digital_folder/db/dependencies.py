from fastapi import Depends

from digital_folder.core.dependencies import validate_user
from digital_folder.db.service import DbService


def get_db_with_user(user=Depends(validate_user)):
    with DbService(user) as db:
        yield db
