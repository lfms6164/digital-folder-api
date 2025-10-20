from typing import List, Optional, Type
from uuid import UUID

from sqlalchemy import asc, desc

from digital_folder.core.pagination.types import QueryParams
from digital_folder.db.db import SessionLocal
from digital_folder.db.models import Group, Project, Tag
from digital_folder.db.types import ModelType
from digital_folder.packages.User.schemas import UserDb


class DbService:
    def __init__(self, user: Optional[UserDb] = None):
        self.user = user

    def __enter__(self):
        self.db = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def get_all(
        self, model: Type[ModelType], params: Optional[QueryParams] = None
    ) -> tuple[List[ModelType], int]:
        """
        Retrieve all rows from the given SQLAlchemy model.

        Args:
            model (Type[ModelType]): The SQLAlchemy ORM model class to query.
            params (Optional[QueryParams]): Query parameters that may contain filters or search.

        Returns:
            tuple[List[ModelType], int]: A list of db rows from the provided model. The total number of rows.
        """

        query = self.db.query(model)
        count = 0

        if self.user.filter_id:
            query = query.filter(model.created_by == self.user.filter_id)

        if params:
            if params.filters:
                created_by = params.filters.pop("created_by", None)
                if created_by:
                    query = query.filter(model.created_by.in_(created_by))

                if params.filters:
                    filters_map = {
                        Group: lambda: (
                            query.filter(Group.tags.any())
                            if params.filters["has_tags"]
                            else query.filter(~Group.tags.any())
                        ),
                        Project: lambda: query.filter(
                            Project.tags.any(Tag.id.in_(params.filters["tag_ids"]))
                        ),
                        Tag: lambda: query.filter(
                            Tag.group_id.in_(params.filters["group_ids"])
                        ),
                    }

                    query = filters_map[model]()

            if params.search:
                query = query.filter(model.name.ilike(f"%{params.search}%"))

            count = query.count()

            # TODO: Allow relationship sorting ex: Tag.group
            if params.sort_by:
                for sort in params.sort_by:
                    table_column_to_be_sorted = getattr(model, sort.key, None)
                    if table_column_to_be_sorted is not None:
                        if sort.order == "desc":
                            query = query.order_by(desc(table_column_to_be_sorted))
                        else:
                            query = query.order_by(asc(table_column_to_be_sorted))
            else:
                query = query.order_by(model.name.asc())

            # -1 means all rows should be selected. In that case this is skipped
            if params.items_per_page != -1:
                offset = (params.page - 1) * params.items_per_page
                query = query.offset(offset).limit(params.items_per_page)

        return query.all(), count

    def get_by_id(self, model: Type[ModelType], obj_id: UUID) -> Optional[ModelType]:
        """
        Retrieve a single row by ID.

        Args:
            model (Type[ModelType]): The SQLAlchemy ORM model class to query.
            obj_id (UUID): ID of the object to filter by.

        Returns:
            Optional[ModelType]: A single db row, if found, from the provided model.
        """

        return self.db.query(model).filter_by(id=obj_id).first()

    def get_by_field(
        self, model: Type[ModelType], value: str, column_name: str
    ) -> Optional[ModelType]:
        """
        Retrieve a single row by a dynamic field.

        Args:
            model (Type[ModelType]): The SQLAlchemy ORM model class to query.
            value (str): The value to match.
            column_name (str): The column name to filter by.

        Returns:
            Optional[ModelType]: A single db row, if found, from the provided model.
        """

        column = getattr(model, column_name, None)
        if column is None:
            raise AttributeError(
                f"Model {model.__name__} doesn't have column: '{column_name}'."
            )

        return self.db.query(model).filter(column == value).first()

    def create(self, model: Type[ModelType], obj_in: dict) -> ModelType:
        """
        Create a new row in the given model.

        Args:
            model (Type[ModelType]): The SQLAlchemy ORM model class to query.
            obj_in (dict): Dict containing the object data to be created.

        Returns:
            ModelType: The created row of the provided model.
        """

        db_obj = model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, model: Type[ModelType], obj_id: UUID, updates: dict) -> None:
        """
        Update an existing row with provided fields.

        Args:
            model (Type[ModelType]): The SQLAlchemy ORM model class to query.
            obj_id (UUID): ID of the object to update.
            updates (dict): Dict containing the object data to be updated.
        """

        obj = self.get_by_id(model, obj_id)

        for field, value in updates.items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)

    def delete(self, model: Type[ModelType], obj_id: UUID) -> None:
        """
        Delete a row from the database.

        Args:
            model (Type[ModelType]): The SQLAlchemy ORM model class to query.
            obj_id (UUID): ID of the object to delete.
        """

        obj = self.get_by_id(model, obj_id)

        self.db.delete(obj)
        self.db.commit()

    def update_relations(
        self,
        entity_model: Type[ModelType],
        related_model: Type[ModelType],
        entity_id: UUID,
        related_ids: List[UUID],
        relation_name: str,
    ) -> None:
        """
        Update a many-to-many relationship between two SQLAlchemy models.

        Args:
            entity_model (Type[ModelType]): The model class of the main entity.
            related_model (Type[ModelType]): The model class of the related entities.
            entity_id (UUID): The ID of the entity to update.
            related_ids (List[UUID]): IDs of the related entities to associate.
            relation_name (str): The relation attribute name of the entity.
        """

        # Only used as: project = db_get_by_id(Project, project_id)
        entity_obj = self.get_by_id(entity_model, entity_id)
        # Only used as: tags = db.query(Tag).filter(Tag.id.in_(tag_ids_list)).all()
        related_objs = (
            self.db.query(related_model).filter(related_model.id.in_(related_ids)).all()
        )

        # Only used as: project.tags = tags
        setattr(entity_obj, relation_name, related_objs)
        self.db.commit()
        self.db.refresh(entity_obj)
