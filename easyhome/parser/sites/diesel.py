"""Use this module to parse the Diesel site."""
from __future__ import annotations

import re
from typing import TYPE_CHECKING
from urllib.parse import urljoin, urlparse

from easyhome.easyhome.models import Currency, Site
from easyhome.parser.entity import ApartmentEntity
from easyhome.parser.sites.base import AbstractSite

if TYPE_CHECKING:
    from bs4 import BeautifulSoup

int_regex = re.compile(r"\d+")
text_regex = re.compile(r"[a-zA-Zа-яА-Я]+")
editor_regex = re.compile(r"Сообщение отредактировал.*")


class Diesel(AbstractSite):
    """Use this class to parse the Diesel site."""

    name = Site.diesel
    first_page = "https://diesel.elcat.kg/index.php?showforum=305"

    _host = "https://diesel.elcat.kg"
    _negative_theme = "2477961"

    def _parse_ulr_and_external_id(self, href: str) -> tuple[str, str]:
        url = urlparse(href)
        external_id = url.query.split("showtopic=")[-1]
        return f"{urljoin(self._host, url.path)}?showtopic={external_id}", external_id

    def get_announcement_pages_map(self, page: BeautifulSoup) -> dict[str, str]:
        """Use this method to get a map of announcement pages from the main page."""
        announcement_map: dict[str, str] = {}
        for item in page.select(".topic_title"):
            url, external_id = self._parse_ulr_and_external_id(item.attrs.get("href"))
            announcement_map[external_id] = url

        announcement_map.pop(self._negative_theme, None)
        return announcement_map

    @staticmethod
    def _get_span_contains_str(page: BeautifulSoup, text: str) -> str:
        elem = page.select_one(f"span:-soup-contains('{text}')")
        if elem is None:
            return ""

        return elem.parent.select_one(".field-value").get_text(strip=True)

    def _parse_price_and_currency(self, page: BeautifulSoup) -> tuple[int, Currency]:
        elem = page.select_one("span.field-value.badge.badge-green")
        if elem is None:
            return 0, Currency.undefined

        full_price = elem.get_text(strip=True)
        price = int(p[0]) if (p := int_regex.search(full_price)) else 0
        currency = self.currency_map[c[0]] if (c := text_regex.search(full_price)) else Currency.undefined
        return price, currency

    @staticmethod
    def _parse_body(page: BeautifulSoup) -> str:
        body = page.select_one(".post")
        body = body.get_text().strip()
        body = editor_regex.sub("", body)
        body = body.replace("Прикрепленные изображения", "")
        body = body.replace(" ", "")
        return body.strip()

    def parse_apartment(self, parsed_response: BeautifulSoup) -> ApartmentEntity:
        """Use this method to parse the apartment from the parsed response."""
        href = parsed_response.select_one("meta[name='identifier-url']").attrs["content"]
        _external_url, _external_id = self._parse_ulr_and_external_id(href)

        _title = parsed_response.select_one(".ipsType_pagetitle") or ""
        if _title != "":
            _title = _title.get_text(strip=True).replace(" ", "")

        _price, _currency = self._parse_price_and_currency(parsed_response)

        _phone = parsed_response.select_one(".custom-field.md-phone > span.field-value") or ""
        if _phone != "":
            _phone = f"+996{_phone.get_text(strip=True)[-9:]}"

        _rooms = self._get_span_contains_str(parsed_response, "Количество комнат")
        _rooms = int(_rooms) if _rooms.isdigit() else 0

        _area = self._get_span_contains_str(parsed_response, "Площадь (кв.м.)")
        _area = int(_area) if _area.isdigit() else 0

        _city = self._get_span_contains_str(parsed_response, "Город:")
        _room_type = self._get_span_contains_str(parsed_response, "Тип помещения")
        _body = self._parse_body(parsed_response)

        _images = [item.attrs["src"] for item in parsed_response.select(".attach")]
        return ApartmentEntity(
            external_id=_external_id,
            site=self.name,
            external_url=_external_url,
            title=_title,
            price=_price,
            currency=_currency,
            phone=_phone,
            rooms=_rooms,
            area=_area,
            city=_city,
            room_type=_room_type,
            body=_body,
            images_list=_images,
        )
