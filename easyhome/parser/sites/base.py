"""Use this module as a base for creating a new site parser."""
from __future__ import annotations

import abc
from typing import ClassVar, TYPE_CHECKING

from easyhome.easyhome.models import Currency

if TYPE_CHECKING:
    from bs4 import BeautifulSoup

    from easyhome.parser.entity import ApartmentEntity


class AbstractSite(abc.ABC):
    """Use this class to create a new site parser."""

    name: str
    use_proxy: bool = False

    first_page: str

    currency_map: ClassVar[dict[str, Currency]] = {
        "": Currency.undefined,
        "сом": Currency.kgs,
        "СОМ": Currency.kgs,
        "kgs": Currency.kgs,
        "KGS": Currency.kgs,
        "usd": Currency.usd,
        "USD": Currency.usd,
    }

    @abc.abstractmethod
    def get_announcement_pages_map(self, page: BeautifulSoup) -> dict[int, str]:
        """Use this method to get a map of announcement pages from the main page."""
        raise NotImplementedError

    @abc.abstractmethod
    def parse_apartment(self, parsed_response: BeautifulSoup) -> ApartmentEntity:
        """Use this method to parse the apartment from the parsed response."""
        raise NotImplementedError
