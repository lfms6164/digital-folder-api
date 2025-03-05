from typing import List
from uuid import UUID

from digital_folder.helpers.db_operations import (
    add_to_db,
    delete_from_db,
    read_from_db,
)
from digital_folder.packages.Relation.schemas import RelationBase


class RelationDTO:
    @staticmethod
    def get_entity_relations(entity_id: UUID, entity_name: str) -> List[UUID]:
        other_entity_name = "tag_id" if entity_name == "project_id" else "project_id"
        relation_df = read_from_db("ProjectTagRelation")

        return relation_df[relation_df[f"{entity_name}"] == str(entity_id)][
            f"{other_entity_name}"
        ].tolist()

    @staticmethod
    def create(project_id: UUID, tag_id: UUID) -> RelationBase:
        relation_obj = RelationDTO.relation_parser(project_id, tag_id)
        add_to_db(relation_obj)

        return relation_obj

    @staticmethod
    def delete_by_id(project_id: UUID, tag_id: UUID) -> None:
        delete_from_db(project_id=project_id, tag_id=tag_id)

    @staticmethod
    def relation_parser(project_id: UUID, tag_id: UUID) -> RelationBase:
        parsed_relation = {
            "project_id": project_id,
            "tag_id": tag_id,
        }

        return RelationBase(
            project_id=parsed_relation["project_id"], tag_id=parsed_relation["tag_id"]
        )
