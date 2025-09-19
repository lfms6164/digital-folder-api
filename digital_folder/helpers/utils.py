import json
from typing import List, Literal, Optional, Type, Union

from pydantic import BaseModel, create_model


class PaginatedResponse(BaseModel):
    items: List[Union["GroupOut", "ProjectOut", "TagOut", "TicketOut"]]
    count: int


class SortParam(BaseModel):
    key: str
    order: Literal["asc", "desc"] = "asc"


class QueryParams(BaseModel):
    """
    Universal query params schema for filtering, searching and sorting.
    """

    filters: Optional[List[str]] = None
    items_per_page: int = 10
    page: int = 1
    search: Optional[str] = None
    sort_by: Optional[List[SortParam]] = None


def query_params_parser(
    filters: Optional[str] = None,
    items_per_page: int = 10,
    page: int = 1,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
) -> QueryParams:
    """
    This function takes data for filtering, searching and sorting and turns it into a QueryParams object.

    Args:
        filters (Optional[str]): Comma-separated filter data.
        items_per_page (int): Number of items to return.
        page (int): Page to return items from.
        search (Optional[str]): Search string.
        sort_by (Optional[str]): JSON string like '[{"key":"name","order":"desc"}]'.

    Returns:
        QueryParams: The parsed query data.
    """

    parsed_sort_by = []
    if sort_by:
        try:
            sort_list = json.loads(sort_by)
            for sort in sort_list:
                parsed_sort_by.append(SortParam(key=sort["key"], order=sort["order"]))
        except Exception as e:
            print(f"Failed to parse sort_by: {e}")

    return QueryParams(
        filters=filters.split(",") if filters else [],
        search=search,
        page=page,
        items_per_page=items_per_page,
        sort_by=parsed_sort_by,
    )


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


from digital_folder.packages.Group.schemas import GroupOut
from digital_folder.packages.Project.schemas import ProjectOut
from digital_folder.packages.Tag.schemas import TagOut
from digital_folder.packages.Ticket.schemas import TicketOut

GroupOut.update_forward_refs()
ProjectOut.update_forward_refs()
TagOut.update_forward_refs()
TicketOut.update_forward_refs()
