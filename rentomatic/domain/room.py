from __future__ import annotations
import dataclasses
from dataclasses import dataclass
from uuid import UUID


@dataclass
class Room:
    code: UUID
    size: int
    price: int
    longitude: float
    latitude: float

    @classmethod
    def from_dict(cls, d: dict) -> Room:
        return cls(**d)

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)
