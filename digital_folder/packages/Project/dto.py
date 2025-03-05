from typing import List, Any, Optional
from uuid import uuid4, UUID

from digital_folder.helpers.db_operations import (
    add_to_db,
    delete_from_db,
    patch_db,
    read_from_db,
)
from digital_folder.packages.Project.schemas import (
    ProjectOut,
    ProjectCreate,
    ProjectPatch,
)
from digital_folder.packages.Relation.dto import RelationDTO
from digital_folder.packages.Tag.dto import TagDTO
from digital_folder.packages.Tag.schemas import TagOut


class ProjectDTO:
    @staticmethod
    def list() -> List[ProjectOut]:
        projects_df = read_from_db("Projects")

        projects = []
        for _, project in projects_df.iterrows():
            relations = RelationDTO.get_entity_relations(project.id, "project_id")
            project = ProjectDTO.project_parser(project=project, tags=relations)
            projects.append(project)

        return projects

    @staticmethod
    def get_by_id(project_id: UUID) -> ProjectOut:
        projects_df = read_from_db("Projects")

        project_obj = ProjectDTO.project_parser(
            project=projects_df[projects_df["id"] == str(project_id)].iloc[0].to_dict(),
            tags=RelationDTO.get_entity_relations(project_id, "project_id"),
        )

        return project_obj

    @staticmethod
    def create(project: ProjectCreate) -> ProjectOut:
        new_project_id = uuid4()

        project_obj = ProjectDTO.project_parser(
            project=project, project_id=new_project_id
        )
        project_dict = project_obj.dict(
            exclude={"tags"}
        )  # No need to store tags data on the projects table since there is a relations table

        add_to_db(project_dict)

        if project_obj.tags:
            for tag in project_obj.tags:
                RelationDTO.create(new_project_id, tag.id)

        return project_obj

    @staticmethod
    def edit_by_id(project_id: UUID, project_data: ProjectPatch) -> ProjectOut:
        patch_db(project_id, project_data)

        if project_data.tags is not None:
            relations = set(RelationDTO.get_entity_relations(project_id, "project_id"))
            new_tags = set(tag.id for tag in project_data.tags)

            tags_to_delete = relations - new_tags
            for tag_id in tags_to_delete:
                RelationDTO.delete_by_id(project_id=project_id, tag_id=tag_id)

            tags_to_add = new_tags - relations
            for tag_id in tags_to_add:
                RelationDTO.create(project_id, tag_id)

        return ProjectDTO.get_by_id(project_id)

    @staticmethod
    def delete_by_id(project_id: UUID) -> None:
        delete_from_db(project_id=project_id)
        relations = RelationDTO.get_entity_relations(project_id, "project_id")

        for relation in relations:
            RelationDTO.delete_by_id(project_id=project_id, tag_id=relation)

    @staticmethod
    def project_parser(
        project: Any,
        project_id: Optional[UUID] = None,
        tags: Optional[List[UUID]] = None,
    ) -> ProjectOut:
        parsed_project = (
            {
                "id": project_id,
                "name": project.name,
                "image": project.image if project.image else None,
                "introduction": project.introduction if project.introduction else None,
                "description": project.description if project.description else None,
                "tags": project.tags if project.tags else None,
            }
            if isinstance(project, (ProjectCreate, ProjectPatch))
            else {
                "id": project["id"],
                "name": project["name"],
                "image": project["image"] if project["image"] else None,
                "introduction": (
                    project["introduction"] if project["introduction"] else None
                ),
                "description": (
                    project["description"] if project["description"] else None
                ),
                "tags": (ProjectDTO.read_tags_from_db(tags) if tags else None),
            }
        )

        return ProjectOut(
            id=parsed_project["id"],
            name=parsed_project["name"],
            image=parsed_project["image"],
            introduction=parsed_project["introduction"],
            description=parsed_project["description"],
            tags=parsed_project["tags"],
        )

    @staticmethod
    def read_tags_from_db(tag_ids: List[UUID]) -> List[TagOut]:
        tag_objects = []
        for tag_id in tag_ids:
            if tag_id:
                tag = TagDTO.get_by_id(tag_id)
                if tag:
                    tag_objects.append(tag)
        return tag_objects
