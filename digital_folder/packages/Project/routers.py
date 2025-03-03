import os
from typing import Any, List

from fastapi import APIRouter, File, HTTPException, UploadFile

from digital_folder.core.config import project_settings
from digital_folder.packages.Project.dto import ProjectDTO
from digital_folder.packages.Project.schemas import (
    ProjectOut,
    ProjectCreate,
    ProjectPatch,
)

project_router = APIRouter()


class ProjectRouter:

    model_dto = ProjectDTO

    @staticmethod
    @project_router.get(path="/list")
    def list() -> List[ProjectOut]:
        """List projects"""

        return ProjectDTO.list()

    @staticmethod
    @project_router.get(path="/project/{project_id}")
    def get_by_id(project_id: str) -> ProjectOut:
        """Get project by id"""

        return ProjectDTO.get_by_id(project_id)

    @staticmethod
    @project_router.post(path="/create")
    def create(project: ProjectCreate) -> ProjectOut:
        """Create project"""

        return ProjectDTO.create(project)

    @staticmethod
    @project_router.patch(path="/patch/{project_id}")
    def patch(project_id: str, project: ProjectPatch) -> ProjectOut:
        """Edit project"""

        return ProjectDTO.edit_by_id(project_id, project)

    @staticmethod
    @project_router.delete(path="/delete/{project_id}")
    def delete(project_id: str) -> None:
        """Delete project"""

        return ProjectDTO.delete_by_id(project_id)

    @staticmethod
    @project_router.post(path="/upload_image")
    async def upload_image(file: UploadFile = File(...)) -> Any:
        """Handles image upload and returns the saved filename"""

        upload_dir = project_settings.static_folder_path
        if not os.path.exists(upload_dir):
            raise HTTPException(
                status_code=400, detail=f"Directory does not exist: {upload_dir}"
            )

        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in ["png", "jpg", "jpeg", "gif"]:
            raise HTTPException(
                status_code=400, detail="Upload image failed - Invalid file type"
            )

        existing_files = set(os.listdir(upload_dir))

        if file.filename not in existing_files:
            file_path = os.path.join(upload_dir, file.filename)

            # Save file
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())

        return {"filename": file.filename}
