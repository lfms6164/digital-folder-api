from fastapi import APIRouter, Depends

from digital_folder.db.db import get_db
from digital_folder.db.service import DbService
from digital_folder.packages.User.dto import UserDTO
from digital_folder.packages.User.schemas import UserLogin

user_router = APIRouter()


class UserRouter:
    def __init__(self, router: APIRouter):
        self.model_dto = UserDTO
        self.router = router
        self.router.add_api_route("/login", self.login, methods=["POST"])

    async def login(
        self,
        form_data: UserLogin = Depends(),
        db: DbService = Depends(get_db),
    ):
        """User login"""

        return self.model_dto(db).login(form_data)


UserRouter(user_router)
