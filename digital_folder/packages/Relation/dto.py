from typing import List
from uuid import UUID

from digital_folder.core.config import project_settings
from digital_folder.helpers.helper_methods import (
    add_to_db,
    delete_relation_from_db,
    read_from_db,
)
from digital_folder.packages.Relation.schemas import RelationBase


class RelationDTO:
    @staticmethod
    def get_entity_relations(entity_id: str, entity_name: str) -> List[str]:
        other_entity_name = "tag_id" if entity_name == "project_id" else "project_id"
        relation_df = read_from_db(project_settings.EXCEL_DB_PATH, "ProjectTagRelation")

        return relation_df[relation_df[f"{entity_name}"] == entity_id][
            f"{other_entity_name}"
        ].tolist()

    @staticmethod
    def create(project_id: UUID, tag_id: UUID) -> RelationBase:
        relation_obj = RelationDTO.relation_parser(project_id, tag_id)
        add_to_db(relation_obj, project_settings.EXCEL_DB_PATH, "ProjectTagRelation")

        return relation_obj

    @staticmethod
    def delete_by_id(project_id: str, tag_id: str) -> None:
        delete_relation_from_db(
            project_id, tag_id, project_settings.EXCEL_DB_PATH, "ProjectTagRelation"
        )

    @staticmethod
    def relation_parser(project_id: UUID, tag_id: UUID) -> RelationBase:
        teste = {
            "project_id": project_id,
            "tag_id": tag_id,
        }

        return RelationBase(project_id=teste["project_id"], tag_id=teste["tag_id"])
