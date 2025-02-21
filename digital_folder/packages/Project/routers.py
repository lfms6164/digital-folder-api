from typing import List

from fastapi import APIRouter

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
