"""Use this module to parse the Lalafo site."""
from __future__ import annotations

import json
import re
from typing import Any, ClassVar, TYPE_CHECKING, TypedDict
from urllib.parse import urljoin

from django.db import models

from easyhome.easyhome.models import Currency, Site
from easyhome.parser.entity import ApartmentEntity
from easyhome.parser.sites.base import AbstractSite

if TYPE_CHECKING:
    from bs4 import BeautifulSoup

int_regex = re.compile(r"\d+")


class ItemDef(TypedDict):  # noqa: D101
    id: int
    url: str


class LalafoParams(models.IntegerChoices):  # noqa: D101
    neighborhood = 357, "Район"
    number_of_rooms = 69, "Количество комнат"
    floor = 226, "Этаж"
    subdivision = 945, "Подселение"
    number_of_floors = 229, "Количество этажей"
    series = 867, "Серия"
    household_appliances = 948, "Бытовая техника"
    apartment_amenities = 949, "Удобства в квартире"
    repair = 872, "Ремонт"
    house_improvement = 950, "Благоустройство дома"
    communications = 870, "Коммуникации"
    furniture = 68, "Мебель"
    for_term = 951, "На срок"
    who_rents = 952, "Кто сдает"
    within_walking_distance = 953, "В шаговой доступности"
    pets = 227, "Животные"


class Lalafo(AbstractSite):
    """Use this class to parse the Lalafo site."""

    name = Site.lalafo
    first_page = "https://lalafo.kg/kyrgyzstan/kvartiry/arenda-kvartir/dolgosrochnaya-arenda-kvartir"

    _host = "https://lalafo.kg"
    _default_next_data_json: ClassVar[dict[str, dict]] = {
        "props": {
            "initialState": {
                "listing": {
                    "listingFeed": {
                        "data": {
                            "items": [],
                        },
                    },
                },
            },
        },
    }

    # Params Ids
    rooms_id = 69
    area_id = 70
    floor_number_id = 226
    floor_total_id = 229
    district_id = 357

    def get_announcement_pages_map(self, page: BeautifulSoup) -> dict[str, str]:
        """Use this method to get a map of announcement pages from the main page."""
        next_script_elem = page.select_one("#__NEXT_DATA__")

        elem_json = json.loads(next_script_elem.getText())
        props = elem_json.get("props", self._default_next_data_json)
        items: list[ItemDef] = props["initialState"]["listing"]["listingFeed"]["data"]["items"]

        announcement_map: dict[str, str] = {}
        for item in items:
            announcement_map[str(item["id"])] = urljoin(self._host, item["url"])

        return announcement_map

    def parse_apartment(self, parsed_response: BeautifulSoup) -> ApartmentEntity:
        """Use this method to parse the apartment from the parsed response."""
        apartment_script_elem = parsed_response.select_one("#__NEXT_DATA__")
        elem_json: dict[str, Any] = json.loads(apartment_script_elem.getText())

        initial_state: dict[str, Any] = elem_json.get("props", {"initialState": {}})["initialState"]

        _external_id: str = str(initial_state["feed"]["adDetails"]["currentAdId"])
        apartment_dict: dict[str, Any] = initial_state["feed"]["adDetails"][_external_id]["item"]

        _currency = self.currency_map[c] if (c := apartment_dict.get("currency", "")) else Currency.undefined

        _params_map = {i["id"]: i["value"] for i in apartment_dict["params"]}

        _rooms = _params_map.get(LalafoParams.number_of_rooms) or ""
        _rooms = int(r[0]) if (r := int_regex.search(_rooms)) else 0

        _floor = int(f) if (f := _params_map.get(LalafoParams.floor)) and f.isdigit() else 0
        _max_floor = int(mf) if (mf := _params_map.get(LalafoParams.number_of_floors)) and mf.isdigit() else 0

        _images = sorted(img["original_url"] for img in apartment_dict.get("images", []))
        return ApartmentEntity(
            external_id=_external_id,
            site=self.name,
            external_url=urljoin(self._host, apartment_dict["url"]),
            title=apartment_dict["title"],
            price=apartment_dict.get("price") or 0,
            currency=_currency,
            phone=apartment_dict.get("mobile") or "",
            rooms=_rooms,
            floor=_floor,
            max_floor=_max_floor,
            district=_params_map.get(LalafoParams.neighborhood) or "",
            city=apartment_dict.get("city") or "",
            body=apartment_dict.get("description") or "",
            images_list=_images,
            lat=apartment_dict.get("lat") or 0.0,
            lon=apartment_dict.get("lng") or 0.0,
        )
