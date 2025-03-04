from typing import List, Optional, Type

from pydantic import BaseModel, create_model


def create_schema_with_exclusions(
    schema_name: str,
    base_schema: Type[BaseModel],
    excluding_fields: List[str],
    optional: bool = False,
) -> Type[BaseModel]:
    """
    Dynamically create a new schema excluding specific fields from the base schema.
    """

    schema_fields = {}

    for k, v in base_schema.model_fields.items():
        if k not in excluding_fields:
            field_type = Optional[v.annotation] if optional else v.annotation
            field_default = None if optional else v.default

            schema_fields[k] = (field_type, field_default)

    new_schema = create_model(schema_name, **schema_fields)

    return new_schema
