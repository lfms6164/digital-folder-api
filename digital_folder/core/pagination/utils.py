import json
from typing import Optional

from digital_folder.core.pagination.types import QueryParams, SortParam
from digital_folder.db.service import DbService
from digital_folder.packages.User.schemas import UserRole


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

            user_dto = UserDTO(db)

            created_by_role = [parsed_filters.get("created_by")]
            if UserRole.USER.value in created_by_role:
                created_by_role.append(UserRole.VIEWER.value)

            parsed_filters["created_by"] = [
                user_dto.get_by_field(UserRole(role), "role").id
                for role in created_by_role
            ]

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
