from typing import Any, List, Optional, Type, TypeVar
from uuid import UUID

from sqlalchemy import asc, desc, select

from digital_folder.db.db import get_db
from digital_folder.db.models import Base, project_tag_relations
from digital_folder.helpers.utils import QueryParams

ModelType = TypeVar("ModelType", bound=Base)


class DbService:
    def __init__(self):
        self.db = next(get_db())

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
        count = query.count()

        if params:
            if params.filters:
                query = query.filter(model.id.in_(params.filters))

            if params.search:
                query = query.filter(model.name.ilike(f"%{params.search}%"))

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

            # -1 means all rows should be selected so this is skipped
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

    def update(self, model: Type[ModelType], obj_id: UUID, updates: dict) -> ModelType:
        """
        Update an existing row with provided fields.

        Args:
            model (Type[ModelType]): The SQLAlchemy ORM model class to query.
            obj_id (UUID): ID of the object to update.
            updates (dict): Dict containing the object data to be updated.

        Returns:
            ModelType: The updated row of the provided model.
        """

        obj = self.get_by_id(model, obj_id)

        for field, value in updates.items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

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

    def get_relation_ids(
        self, ids_list: List[str], search_col: str, return_col: str
    ) -> Any:
        """
        Retrieve IDs from a relation table based on a list of source IDs.

        Args:
            ids_list (List[str]): List of IDs to filter by on 'search_col'.
            search_col (str): Table column name in the relation table to filter by.
            return_col (str): Table column name in the relation table whose values are to be returned.

        Returns:
        Any: A list of IDs from 'return_col'.
        """

        query = (
            select(project_tag_relations.c[return_col])
            .where(project_tag_relations.c[search_col].in_(ids_list))
            .distinct()
        )

        return self.db.execute(query).scalars().all()

    def relations_update(
        self,
        model: Type[ModelType],
        model2: Type[ModelType],
        ids_list: List[UUID],
        obj_id: UUID,
        relation_attr: str,
    ) -> None:
        """
        Update a many-to-many relationship between two SQLAlchemy models.

        Args:
            model (Type[ModelType]): The model class of the parent object.
            model2 (Type[ModelType]): The model class of the related objects.
            ids_list (List[UUID]): List of IDs of 'model2' objects to assign to the relation.
            obj_id (UUID): The ID of the parent object whose relation is to be updated.
            relation_attr (str): The name of the relation attribute on the parent object.
        """

        # Only used as: tags = db.query(Tag).filter(Tag.id.in_(tag_ids_list)).all()
        objs = self.db.query(model2).filter(model2.id.in_(ids_list)).all()
        # Only used as: project = db_get_by_id(db, Project, project_id)
        obj = self.get_by_id(model, obj_id)
        # Only used as: project.tags = tags
        setattr(obj, relation_attr, objs)
        self.db.commit()
        self.db.refresh(obj)
