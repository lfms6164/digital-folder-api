from typing import List, Optional, Type, TypeVar

from pydantic import BaseModel, create_model

from digital_folder.db.db import Base

ModelType = TypeVar("ModelType", bound=Base)


def create_schema_with_exclusions(
    schema_name: str,
    base_schema: Type[BaseModel],
    excluding_fields: List[str],
    optional: bool = False,
) -> Type[BaseModel]:
    """
    Dynamically create a new Pydantic schema excluding specific fields from a base schema.

    Args:
        schema_name (str): The name for the new schema.
        base_schema (Type[BaseModel]): The base Pydantic schema to create the new one from.
        excluding_fields (List[str]): A list of field names from the base schema to be excluded on the new schema.
        optional (bool): If True, all new schema fields will be optional. Default is False.

    Returns:
        Type[BaseModel]: The new Pydantic schema with excluded fields and optionally Optional.
    """

    schema_fields = {}

    for key, val in base_schema.model_fields.items():
        if key not in excluding_fields:
            field_type = Optional[val.annotation] if optional else val.annotation
            field_default = None if optional else val.default

            schema_fields[key] = (field_type, field_default)

    new_schema = create_model(schema_name, **schema_fields)

    return new_schema
