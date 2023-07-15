import abc

from bs4 import BeautifulSoup

from hsearch.parser.entity import ApartmentEntity


class AbstractSite(abc.ABC):
    name: str
    use_proxy: bool = False

    first_page: str

    @abc.abstractmethod
    def get_announcement_pages_map(self, page: BeautifulSoup) -> dict[int, str]:
        raise NotImplementedError

    @abc.abstractmethod
    def parse_apartment(self, parsed_response: BeautifulSoup) -> ApartmentEntity:
        raise NotImplementedError
