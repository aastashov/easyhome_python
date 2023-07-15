import json
from typing import Any, TypedDict
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag

from hsearch.hsearch.models import Site
from hsearch.parser.entity import ApartmentEntity
from hsearch.parser.sites.base import AbstractSite


class ItemDef(TypedDict):
    id: int
    url: str


class Lalafo(AbstractSite):
    name = Site.lalafo
    first_page = "https://lalafo.kg/kyrgyzstan/kvartiry/arenda-kvartir/dolgosrochnaya-arenda-kvartir"

    _host = "https://lalafo.kg"
    _default_next_data_json = {"props": {"initialState": {"listing": {"listingFeed": {"items": []}}}}}

    def get_announcement_pages_map(self, page: BeautifulSoup) -> dict[int, str]:
        next_script_elem = page.select_one("#__NEXT_DATA__")

        elem_json = json.loads(next_script_elem.getText())
        props = elem_json.get("props", self._default_next_data_json)
        items: list[ItemDef] = props["initialState"]["listing"]["listingFeed"]["items"]

        announcement_map: dict[int, str] = {}
        for item in items:
            announcement_map[item["id"]] = urljoin(self._host, item["url"])

        return announcement_map

    def parse_apartment(self, parsed_response: BeautifulSoup) -> ApartmentEntity:
        apartment_script_elem = parsed_response.select_one("#__NEXT_DATA__")
        elem_json: dict[str, Any] = json.loads(apartment_script_elem.getText())

        initial_state: dict[str, Any] = elem_json.get("props", {"initialState": {}})["initialState"]

        _external_id: int = initial_state["feed"]["adDetails"]["currentAdId"]
        apartment_dict: dict[str, Any] = initial_state["feed"]["adDetails"][str(_external_id)]["item"]

        return ApartmentEntity(
            external_id=_external_id,
            external_url=urljoin(self._host, apartment_dict["url"]),
            title=apartment_dict["title"],
        )
