from typing import TypeVar

from digital_folder.db.db import Base

ModelType = TypeVar("ModelType", bound=Base)
