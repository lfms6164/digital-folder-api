import json
from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel

from digital_folder.packages.Group.schemas import GroupOut
from digital_folder.packages.Project.schemas import ProjectOut
from digital_folder.packages.Tag.schemas import TagOut
from digital_folder.packages.Ticket.schemas import TicketOut
from digital_folder.packages.User.schemas import UserRole


class PaginatedResponse(BaseModel):
    items: List[Union[GroupOut, ProjectOut, TagOut, TicketOut]]
    count: int


class SortParam(BaseModel):
    key: str
    order: Literal["asc", "desc"] = "asc"


class QueryParams(BaseModel):
    """
    Universal query params schema for filtering, searching and sorting.
    """

    filters: Optional[dict[str, Any]] = None  # dict[str, Union[bool, str, UUID]]
    items_per_page: int = 10
    page: int = 1
    search: Optional[str] = None
    sort_by: Optional[List[SortParam]] = None


from digital_folder.db.service import DbService


def query_params_parser(
    db: DbService,
    filters: Optional[str] = None,
    items_per_page: int = 10,
    page: int = 1,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
) -> QueryParams:
    """
    This function takes data for filtering, searching and sorting and turns it into a QueryParams object.

    Args:
        db (DbService): The db session.
        filters (Optional[str]): Filters.
        items_per_page (int): Number of items to return.
        page (int): Page to return items from.
        search (Optional[str]): Search string.
        sort_by (Optional[str]): JSON string like '[{"key":"name","order":"desc"}]'.

    Returns:
        QueryParams: The parsed query data.
    """

    parsed_filters = {}
    if filters:
        parsed_filters = json.loads(filters)
        if parsed_filters and parsed_filters.get("created_by"):
            from digital_folder.packages.User.dto import UserDTO

            parsed_filters["created_by"] = (
                UserDTO(db)
                .get_by_field(UserRole(parsed_filters["created_by"]), "role")
                .id
            )

    parsed_sort_by = []
    if sort_by:
        sort_dict = json.loads(sort_by)
        for sort in sort_dict:
            parsed_sort_by.append(SortParam(key=sort["key"], order=sort["order"]))

    return QueryParams(
        filters=parsed_filters,
        search=search,
        page=page,
        items_per_page=items_per_page,
        sort_by=parsed_sort_by,
    )
