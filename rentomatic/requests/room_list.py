from collections.abc import Mapping


class RoomListInvalidRequest:
    def __init__(self):
        self.errors = []  # type: list[dict]

    def add_error(self, parameter: str, message: str):
        self.errors.append({"parameter": parameter, "message": message})

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def __bool__(self) -> bool:
        return False


class RoomListValidRequest:
    def __init__(self, filters: dict | None = None):
        self.filters = filters

    def __bool__(self) -> bool:
        return True


def build_room_list_request(
    filters: dict | None = None
) -> RoomListValidRequest | RoomListInvalidRequest:
    accepted_filters = ["code__eq", "price__eq", "price__lt", "price__gt"]
    invalid_req = RoomListInvalidRequest()

    if filters is not None:
        if not isinstance(filters, Mapping):
            invalid_req.add_error("filters", "Is not iterable")
            return invalid_req

        for key in filters:
            if key not in accepted_filters:
                invalid_req.add_error("filters", f"Key {key} cannot be used")

        if invalid_req.has_errors():
            return invalid_req

    return RoomListValidRequest(filters=filters)
