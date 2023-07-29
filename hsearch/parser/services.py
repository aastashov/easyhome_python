from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol

from bs4 import BeautifulSoup
from django.db.models import QuerySet
from django.utils import timezone

from hsearch.hsearch.models import Apartment
from hsearch.parser.sites.base import AbstractSite


class HttpClientProtocol(Protocol):
    def fetch_first_page(self, page_url: str) -> BeautifulSoup:
        raise NotImplementedError

    def fetch_announcement_pages(self, pages_map: dict[int, str]) -> dict[int, BeautifulSoup]:
        raise NotImplementedError


@dataclass(slots=True)
class ParseSiteService:
    http_client: HttpClientProtocol
    site: AbstractSite

    def parse(self) -> None:
        first_page = self.http_client.fetch_first_page(self.site.first_page)
        announcement_pages_map = self.site.get_announcement_pages_map(first_page)

        non_existing_announcement = self.filter_non_existing_announcement(announcement_pages_map)
        announcement_map = self.http_client.fetch_announcement_pages(non_existing_announcement)

        self.create_announcement(announcement_map)
        # self.update_viewed_at(set(announcement_pages_map.keys()) - set(non_existing_announcement.keys()))

    def filter_non_existing_announcement(self, pages_map: dict[int, str]) -> dict[int, str]:
        apartment_queryset: QuerySet[Apartment] = Apartment.objects.filter(
            site=self.site.name,
            external_id__in=pages_map.keys(),
        )
        existing_announcement = {i.external_id: i for i in apartment_queryset}
        return {k: v for k, v in pages_map.items() if k not in existing_announcement}

    def create_announcement(self, new_announcement: dict[int, BeautifulSoup]) -> None:
        apartments_to_create: list[Apartment] = []
        for external_id, parsed_response in new_announcement.items():
            parsed_apartment = self.site.parse_apartment(parsed_response)
            apartments_to_create.append(
                # TODO: Add more fields from ApartmentEntity
                Apartment(
                    external_id=parsed_apartment.external_id,
                    topic=parsed_apartment.title,
                    url=parsed_apartment.external_url,
                    site=self.site.name,
                    # viewed_at=timezone.now(),
                ),
            )

        Apartment.objects.bulk_create(apartments_to_create)

    def update_viewed_at(self, announcement_external_ids: Iterable[int]) -> None:
        apartment_queryset: QuerySet[Apartment] = Apartment.objects.filter(
            site=self.site.name,
            external_id__in=announcement_external_ids,
        )

        apartment_queryset.update(viewed_at=timezone.now())
