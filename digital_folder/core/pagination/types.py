from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel

from digital_folder.packages.Group.schemas import GroupOut
from digital_folder.packages.Project.schemas import ProjectOut
from digital_folder.packages.Tag.schemas import TagOut
from digital_folder.packages.Ticket.schemas import TicketOut


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
