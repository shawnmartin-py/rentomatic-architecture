from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, Protocol, TYPE_CHECKING
from rentomatic.repository.postgres_objects import Room
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


class Repo(Protocol):
    def list(self, filters: dict) -> list: ...

@overload
def room_list_use_case(
    repo: Repo, request: RoomListValidRequest
) -> ResponseSuccess | ResponseFailure: ...

@overload
def room_list_use_case(
    repo: Repo, request: RoomListInvalidRequest
) -> ResponseFailure: ...

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