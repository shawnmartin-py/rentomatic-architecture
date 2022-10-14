import os

from fastapi import APIRouter, HTTPException, status

from rentomatic.repository.postgresrepo import PostgresRepo
from rentomatic.use_cases.room_list import room_list_use_case
from rentomatic.requests.room_list import build_room_list_request
from rentomatic.responses import ResponseTypes


router = APIRouter()

STATUS_CODES = {
    ResponseTypes.RESOURCE_ERROR: status.HTTP_404_NOT_FOUND,
    ResponseTypes.PARAMETERS_ERROR: status.HTTP_400_BAD_REQUEST,
    ResponseTypes.SYSTEM_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
}

postgres_configuration = {
    "POSTGRES_USER": os.environ["POSTGRES_USER"],
    "POSTGRES_PASSWORD": os.environ["POSTGRES_PASSWORD"],
    "POSTGRES_HOSTNAME": os.environ["POSTGRES_HOSTNAME"],
    "POSTGRES_PORT": os.environ["POSTGRES_PORT"],
    "APPLICATION_DB": os.environ["APPLICATION_DB"],
}


@router.get("/rooms")
def room_list(
    filter_code__eq: str | None = None,
    filter_price__eq: str | None = None,
    filter_price__lt: str | None = None,
    filter_price__gt: str | None = None,
):
    filters = {}
    if filter_code__eq is not None:
        filters.update(code__eq=filter_code__eq)
    if filter_price__eq is not None:
        filters.update(price__eq=filter_price__eq)
    if filter_price__gt is not None:
        filters.update(price__gt=filter_price__gt)
    if filter_price__lt is not None:
        filters.update(price__lt=filter_price__lt)

    request_object = build_room_list_request(filters=filters)
    repo = PostgresRepo(postgres_configuration)
    response = room_list_use_case(repo, request_object)
    if response.type == ResponseTypes.SUCCESS:
        return response.value
    raise HTTPException(STATUS_CODES[response.type], response.value)
