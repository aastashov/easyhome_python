"""Use this module to parse the House site."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, TypedDict
from urllib.parse import urljoin

from easyhome.easyhome.models import Currency, Site
from easyhome.parser.entity import ApartmentEntity
from easyhome.parser.sites.base import AbstractSite

if TYPE_CHECKING:
    from bs4 import BeautifulSoup

int_regex = re.compile(r"\d+")


class ItemDef(TypedDict):  # noqa: D101
    id: int
    url: str


class House(AbstractSite):
    """Use this class to parse the House site."""

    name = Site.house
    first_page = "https://www.house.kg/snyat-kvartiru?region=1&town=2&rental_term=3&sort_by=upped_at+desc&page=1"

    _host = "https://www.house.kg"

    def get_announcement_pages_map(self, page: BeautifulSoup) -> dict[str, str]:
        """Use this method to get a map of announcement pages from the main page."""
        apartment_urls: list[str] = [i.attrs["content"] for i in page.select("meta[itemprop=url]")]

        announcement_map: dict[str, str] = {}
        for apartment_url in apartment_urls:
            announcement_map[apartment_url.split("/")[-1]] = urljoin(self._host, apartment_url)

        return announcement_map

    @staticmethod
    def _parse_price_and_currency(parsed_response: BeautifulSoup) -> tuple[int, Currency]:
        """Use this method to parse the price and currency from the parsed response."""
        price_elem = parsed_response.select_one(".price-dollar")
        currency = Currency.usd
        if not price_elem:
            price_elem = parsed_response.select_one(".price-som")
            currency = Currency.kgs

        price_str = price_elem.get_text(strip=True).replace(" ", "")
        price = int(p[0]) if (p := int_regex.search(price_str)) else 0
        return price, currency

    @staticmethod
    def _fund_text_contain(parsed_response: BeautifulSoup, text: str) -> str:
        label_elem = parsed_response.select_one(f".label:-soup-contains('{text}')")
        if not label_elem:
            return ""

        info_elem = label_elem.parent.select_one(".info")
        if not info_elem:
            return ""
        return info_elem.get_text(strip=True)

    def _parse_floor_and_max_floor(self, parsed_response: BeautifulSoup) -> tuple[int, int]:
        floor_string = self._fund_text_contain(parsed_response, "Этаж")
        if not floor_string:
            return 0, 0

        floor = int(floor_string.split("этаж")[0])
        max_floor = 0

        max_floor_data = floor_string.split(" из ")
        if len(max_floor_data) > 1:
            max_floor = int(max_floor_data[-1])

        return floor, max_floor

    @staticmethod
    def _parse_images(parsed_response: BeautifulSoup) -> list[str]:
        return [i.attrs["href"] for i in parsed_response.select(".fotorama > a")]

    def parse_apartment(self, parsed_response: BeautifulSoup) -> ApartmentEntity:
        """Use this method to parse the apartment from the parsed response."""
        _canonical_url = parsed_response.select_one("link[rel='canonical']").attrs["href"]
        _external_id = _canonical_url.split("/")[-1]

        _title = parsed_response.select_one("h1").get_text(strip=True)

        _price, _currency = self._parse_price_and_currency(parsed_response)
        _floor, _max_floor = self._parse_floor_and_max_floor(parsed_response)

        _phone = ""
        phone_elem = parsed_response.select_one(".number")
        if phone_elem:
            _phone = phone_elem.get_text(strip=True).replace(" ", "").replace("-", "").replace("+", "")

        _rooms = int(r[0]) if (r := int_regex.search(_title)) else 0

        _address = parsed_response.select_one(".address").get_text(strip=True)
        _city, _district = _address.split(",")

        _description = parsed_response.select_one(".description > p").get_text(strip=True)

        _images = self._parse_images(parsed_response)

        _area = 0
        area_str = self._fund_text_contain(parsed_response, "Площадь")
        if area_str:
            _area = int(a[0]) if (a := int_regex.search(area_str)) else 0

        _lat, _lon = 0, 0
        _coordinates_elem = parsed_response.select_one("#map2gis")
        if _coordinates_elem:
            _lat = float(_coordinates_elem.attrs["data-lat"])
            _lon = float(_coordinates_elem.attrs["data-lon"])

        return ApartmentEntity(
            external_id=_external_id,
            site=self.name,
            external_url=_canonical_url,
            title=_title,
            price=_price,
            currency=_currency,
            phone=_phone,
            rooms=_rooms,
            floor=_floor,
            max_floor=_max_floor,
            district=_district.strip(),
            city=_city.strip(),
            body=_description,
            images_list=_images,
            area=_area,
            lat=_lat,
            lon=_lon,
        )
