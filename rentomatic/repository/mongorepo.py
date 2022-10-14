from __future__ import annotations
from typing import TYPE_CHECKING
import pymongo

from rentomatic.domain.room import Room

if TYPE_CHECKING:
    from pymongo.cursor import Cursor


class MongoRepo:
    def __init__(self, configuration: dict):
        client = pymongo.MongoClient(
            host=configuration["MONGODB_HOSTNAME"],
            port=int(configuration["MONGODB_PORT"]),
            username=configuration["MONGODB_USER"],
            password=configuration["MONGODB_PASSWORD"],
            authSource="admin",
        )

        self.db = client[configuration["APPLICATION_DB"]]

    def _create_room_objects(self, results: Cursor) -> list[Room]:
        return [
            Room(
                code=q["code"],
                size=q["size"],
                price=q["price"],
                latitude=q["latitude"],
                longitude=q["longitude"],
            )
            for q in results
        ]

    def list(self, filters: dict | None = None) -> list[Room]:
        collection = self.db.rooms

        if filters is None:
            result = collection.find()
        else:
            mongo_filter = {}
            for key, value in filters.items():
                key, operator = key.split("__")

                filter_value = mongo_filter.get(key, {})

                if key == "price":
                    value = int(value)

                filter_value[f"${operator}"] = value
                mongo_filter[key] = filter_value

            result = collection.find(mongo_filter)

        return self._create_room_objects(result)
