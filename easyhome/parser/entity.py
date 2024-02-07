from __future__ import annotations  # noqa: D100

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from easyhome.easyhome.models import Currency, Site


@dataclass(slots=True)
class ApartmentEntity:  # noqa: D101
    external_id: str
    site: Site
    external_url: str
    title: str
    price: int
    currency: Currency
    phone: str
    rooms: int
    city: str
    body: str
    images_list: list[str]

    room_type: str = ""
    floor: int = 0
    max_floor: int = 0
    district: str = ""
    area: int = 0
    lat: float = 0.0
    lon: float = 0.0
    is_deleted: bool = False
