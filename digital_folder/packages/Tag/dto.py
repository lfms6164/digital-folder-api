from typing import List, Any, Optional
from uuid import uuid4, UUID

from digital_folder.core.config import project_settings
from digital_folder.helpers.helper_methods import (
    add_to_db,
    delete_from_db,
    read_from_db,
    patch_db_entry,
)
from digital_folder.packages.Relation.dto import RelationDTO
from digital_folder.packages.Tag.schemas import TagCreate, TagOut, TagPatch


class TagDTO:
    @staticmethod
    def list() -> List[TagOut]:
        tags_df = read_from_db(project_settings.EXCEL_DB_PATH, "Tags")

        tags = []
        for _, row in tags_df.iterrows():
            tag = TagDTO.tag_parser(row)
            tags.append(tag)

        return tags

    @staticmethod
    def get_by_id(tag_id: str) -> TagOut:
        tags_df = read_from_db(project_settings.EXCEL_DB_PATH, "Tags")

        tag_obj = TagDTO.tag_parser(tags_df[tags_df["id"] == tag_id].iloc[0].to_dict())

        return tag_obj

    @staticmethod
    def create(tag: TagCreate) -> TagOut:
        new_id = uuid4()

        tag_obj = TagDTO.tag_parser(tag, new_id)
        add_to_db(tag_obj, project_settings.EXCEL_DB_PATH, "Tags")

        return tag_obj

    @staticmethod
    def edit_by_id(id_: str, tag_data: TagPatch) -> TagOut:
        patch_db_entry(id_, tag_data, project_settings.EXCEL_DB_PATH, "Tags")

        return TagDTO.get_by_id(id_)

    @staticmethod
    def delete_by_id(id_: str) -> None:
        delete_from_db(id_, project_settings.EXCEL_DB_PATH, "Tags")

        relations = RelationDTO.get_entity_relations(id_, "tag_id")

        for relation in relations:
            RelationDTO.delete_by_id(project_id=relation, tag_id=id_)

    @staticmethod
    def tag_parser(tag: Any, uuid: Optional[UUID] = None) -> TagOut:
        teste = (
            {
                "id": uuid,
                "name": tag.name if tag.name else None,
                "icon": tag.icon if tag.icon else None,
                "color": tag.color,
            }
            if isinstance(tag, TagCreate)
            else {
                "id": UUID(tag["id"]),
                "name": tag["name"] if tag["name"] else None,
                "icon": tag["icon"] if tag["icon"] else None,
                "color": tag["color"],
            }
        )

        return TagOut(
            id=teste["id"], name=teste["name"], icon=teste["icon"], color=teste["color"]
        )
