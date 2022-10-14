from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from rentomatic.responses import (
    ResponseSuccess,
    ResponseFailure,
    ResponseTypes,
    build_response_from_invalid_request,
)

if TYPE_CHECKING:
    from rentomatic.requests.room_list import (
        RoomListValidRequest, 
        RoomListInvalidRequest,
    )


class Repo(ABC):
    @abstractmethod
    def list(self, filters: dict) -> list: ...


def room_list_use_case(
    repo: Repo, request: RoomListValidRequest | RoomListInvalidRequest
) -> ResponseSuccess | ResponseFailure:
    if not request:
        return build_response_from_invalid_request(request)
    try:
        rooms = repo.list(filters=request.filters)
        return ResponseSuccess(rooms)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)
