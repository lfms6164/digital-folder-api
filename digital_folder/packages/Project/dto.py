from typing import Any, List
from uuid import UUID

from fastapi import HTTPException

from digital_folder.core.auth import validate_ownership, validate_unique
from digital_folder.core.pagination import PaginatedResponse, QueryParams
from digital_folder.db.models import Project, Tag
from digital_folder.db.service import DbService
from digital_folder.packages.Project.schemas import (
    ProjectCreate,
    ProjectPatch,
    ProjectOut,
)
from digital_folder.packages.Tag.dto import TagDTO
from digital_folder.supabase.client import SupabaseStorageConfig
from digital_folder.supabase.storage import SupabaseDTO


class ProjectDTO:
    def __init__(self, db: DbService):
        self.db = db
        self.supabase_storage_config = SupabaseStorageConfig(
            bucket=self.db.user.role_config.storage_bucket, folder="projects"
        )

    def list(self, params: QueryParams) -> PaginatedResponse:
        """
        Retrieve all projects from the database.

        Returns:
            List[ProjectOut]: A list of all projects.
        """

        projects, count = self.db.get_all(Project, params)
        parsed_projects = []
        for project in projects:
            project = self.project_parser(project)
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

        return self.project_parser(project)

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

        if project_data.tag_ids:
            validate_ownership(TagDTO(self.db), project_data.tag_ids, True)
        validate_unique(self.db, Project, project_data.name)

        project_dict = project_data.dict(exclude={"tags", "tag_ids"})
        project_dict["repo_url"] = (
            str(project_data.repo_url) if project_data.repo_url else None
        )
        project_dict["created_by"] = self.db.user.id
        project = self.db.create(Project, project_dict)

        if project_data.tag_ids:
            self.db.update_relations(
                Project, Tag, project.id, project_data.tag_ids, "tags"
            )

        if project_data.images:
            SupabaseDTO(self.supabase_storage_config).move_files(
                project.images, str(project.id)
            )

        return self.project_parser(project)

    def edit_by_id(self, project_id: UUID, project_data: ProjectPatch) -> ProjectOut:
        """
        Edit a project by its ID.

        Args:
            project_id (UUID): The project ID.
            project_data (ProjectPatch): The project data.

        Returns:
            ProjectOut: The patched project data.
        """

        validate_ownership(self, [project_id])
        if project_data.tag_ids:
            validate_ownership(TagDTO(self.db), project_data.tag_ids, True)
        if project_data.name:
            validate_unique(self.db, Project, project_data.name)

        project_dict = project_data.dict(exclude_unset=True, exclude={"tag_ids"})
        if project_dict:
            self.db.update(
                Project,
                project_id,
                project_dict,
            )

        if project_data.images is not None:
            supabase_dto = SupabaseDTO(self.supabase_storage_config)
            old = set(supabase_dto.get_files_from_folder(str(project_id)))
            new = set(project_data.images)

            to_add = new - old
            if to_add:
                supabase_dto.move_files(list(to_add), str(project_id))

            to_delete = old - new
            if to_delete:
                supabase_dto.delete_files(list(to_delete), str(project_id))

        if project_data.tag_ids is not None:
            self.db.update_relations(
                Project, Tag, project_id, project_data.tag_ids, "tags"
            )

        return self.get_by_id(project_id)

    def delete_by_id(self, project_id: UUID) -> None:
        """
        Delete a project by its ID. Relations are deleted automatically.

        Args:
            project_id (UUID): The project ID.
        """

        validate_ownership(self, [project_id])

        project = self.get_by_id(project_id)
        if project.images:
            SupabaseDTO(self.supabase_storage_config).delete_folder(str(project_id))

        self.db.delete(Project, project_id)

    def project_parser(self, project: Any) -> ProjectOut:
        """
        This function takes project data and turns it into a ProjectOut object.

        Args:
            project (Any): The project data.

        Returns:
            ProjectOut: The parsed project data.
        """

        tag_dto = TagDTO(self.db) if project.tags else None

        parsed_project = {
            "id": project.id,
            "name": project.name,
            "repo_url": project.repo_url or None,
            "introduction": project.introduction or None,
            "description": project.description or None,
            "tags": (
                [tag_dto.tag_parser(tag) for tag in project.tags]
                if project.tags
                else []
            ),
            "tag_ids": [tag.id for tag in project.tags] if project.tags else [],
            "images": project.images or None,
            "created_by": project.created_by,
        }

        return ProjectOut(
            id=parsed_project["id"],
            name=parsed_project["name"],
            repo_url=parsed_project["repo_url"],
            introduction=parsed_project["introduction"],
            description=parsed_project["description"],
            tags=parsed_project["tags"],
            tag_ids=parsed_project["tag_ids"],
            images=parsed_project["images"],
            created_by=parsed_project["created_by"],
        )
