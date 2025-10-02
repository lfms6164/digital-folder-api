from fastapi import APIRouter

from digital_folder.packages.Server.schemas import ServerResponse, ServerStatus

server_router = APIRouter()


class ServerRouter:
    def __init__(self, router: APIRouter):
        self.router = router
        self.router.add_api_route("/status", self.status_check, methods=["GET"])

    @staticmethod
    def status_check() -> ServerResponse:
        """Check server status"""

        return ServerResponse(status=ServerStatus.ON)


ServerRouter(server_router)
