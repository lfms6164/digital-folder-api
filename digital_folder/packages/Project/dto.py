from typing import Any, List
from uuid import UUID

from fastapi import HTTPException

from digital_folder.db.models import Project, Tag
from digital_folder.helpers.db_operations import DbService
from digital_folder.helpers.utils import QueryParams, PaginatedResponse
from digital_folder.packages.Project.schemas import (
    ProjectOut,
    ProjectCreate,
    ProjectPatch,
)
from digital_folder.packages.Tag.dto import TagDTO
from digital_folder.supabase.storage import SupabaseDTO


class ProjectDTO:
    def __init__(self):
        self.db = DbService()
        self.supabase_storage_bucket = "projects"

    def list(self, params: QueryParams) -> PaginatedResponse:
        """
        Retrieve all projects from the database.

        Returns:
            List[ProjectOut]: A list of all projects.
        """

        if params.filters:
            params.filters = self.db.get_relation_ids(
                params.filters, "tag_id", "project_id"
            )
            # if no match return []
            if not params.filters:
                return PaginatedResponse(items=[], count=0)

        projects, count = self.db.get_all(Project, params)

        parsed_projects = []
        for project in projects:
            project = self.project_parser(project=project)
            parsed_projects.append(project)

        return PaginatedResponse(items=parsed_projects, count=count)

    def get_by_id(self, project_id: UUID) -> ProjectOut:
        """
        Retrieve a project by its ID.

        Args:
            project_id (UUID): The project ID.

        Returns:
            ProjectOut: The project data.
        """

        project = self.db.get_by_id(Project, project_id)
        if not project:
            raise HTTPException(
                status_code=400, detail=f"Project {project_id} not found."
            )

        project_obj = self.project_parser(project=project)

        return project_obj

    def create(self, project_data: ProjectCreate) -> ProjectOut:
        """
        Create a new project.
        This function takes project data, generates a new UUID, turns this data into a structured ProjectOut object
        and ads it to the database excluding the tags data which are stored in their own dedicated database table.

        Args:
            project_data (ProjectCreate): The project data.

        Returns:
            ProjectOut: The created project data.
        """

        project = self.db.create(
            Project, project_data.dict(exclude={"tags", "tag_ids"})
        )

        if project_data.images:
            SupabaseDTO(self.supabase_storage_bucket).move_files(
                project.images, str(project.id)
            )

        if project_data.tag_ids:
            self.db.relations_update(
                Project, Tag, project_data.tag_ids, project.id, "tags"
            )

        return self.project_parser(project=project)

    def edit_by_id(self, project_id: UUID, project_data: ProjectPatch) -> ProjectOut:
        """
        Edit a project by its ID.

        Args:
            project_id (UUID): The project ID.
            project_data (ProjectPatch): The project data.

        Returns:
            ProjectOut: The patched project data.
        """

        project_dict = project_data.dict(exclude_unset=True, exclude={"tag_ids"})
        if project_dict:
            self.db.update(
                Project,
                project_id,
                project_dict,
            )

        if project_data.images is not None:
            supabase_dto = SupabaseDTO(self.supabase_storage_bucket)
            old = set(supabase_dto.list_files_from_folder(str(project_id)))
            new = set(project_data.images)

            to_add = new - old
            if to_add:
                supabase_dto.move_files(list(to_add), str(project_id))

            to_delete = old - new
            if to_delete:
                files_to_delete = [
                    f"{str(project_id)}/{file}" for file in list(to_delete)
                ]
                supabase_dto.delete_files(files_to_delete)

        if project_data.tag_ids is not None:
            self.db.relations_update(
                Project, Tag, project_data.tag_ids, project_id, "tags"
            )

        return self.get_by_id(project_id)

    def delete_by_id(self, project_id: UUID) -> None:
        """
        Delete a project by its ID. Relations are deleted automatically.

        Args:
            project_id (UUID): The project ID.
        """

        project = self.get_by_id(project_id)
        if project.images:
            SupabaseDTO(self.supabase_storage_bucket).delete_folder(str(project_id))

        self.db.delete(Project, project_id)

    @staticmethod
    def project_parser(project: Any) -> ProjectOut:
        """
        This function takes project data and turns it into a ProjectOut object.

        Args:
            project (Any): The project data.

        Returns:
            ProjectOut: The parsed project data.
        """

        tag_dto = TagDTO()

        parsed_project = {
            "id": project.id,
            "name": project.name,
            "images": project.images or None,
            "introduction": project.introduction or None,
            "description": project.description or None,
            "tags": (
                [tag_dto.tag_parser(tag) for tag in project.tags]
                if project.tags
                else []
            ),
            "tag_ids": [tag.id for tag in project.tags] if project.tags else [],
        }

        return ProjectOut(
            id=parsed_project["id"],
            name=parsed_project["name"],
            images=parsed_project["images"],
            introduction=parsed_project["introduction"],
            description=parsed_project["description"],
            tags=parsed_project["tags"],
            tag_ids=parsed_project["tag_ids"],
        )
