import logging
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol

from bs4 import BeautifulSoup
from django.db.models import QuerySet
from django.utils import timezone

from hsearch.hsearch.models import Apartment
from hsearch.parser.sites.base import AbstractSite

logger = logging.getLogger(__name__)


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
            try:
                parsed_apartment = self.site.parse_apartment(parsed_response)
            except Exception as e:
                logger.exception(
                    "Can't parse an apartment with id %s from site %s",
                    external_id,
                    self.site.name,
                    exc_info=e,
                )
                continue

            apartments_to_create.append(
                Apartment(
                    external_id=parsed_apartment.external_id,
                    url=parsed_apartment.external_url,
                    topic=parsed_apartment.title,
                    phone=parsed_apartment.phone,
                    rooms=parsed_apartment.rooms,
                    body=parsed_apartment.body,
                    price=parsed_apartment.price,
                    currency=parsed_apartment.currency,
                    area=parsed_apartment.area,
                    city=parsed_apartment.city,
                    room_type=parsed_apartment.room_type,
                    site=parsed_apartment.site,
                    floor=parsed_apartment.floor,
                    max_floor=parsed_apartment.max_floor,
                    district=parsed_apartment.district,
                    lat=parsed_apartment.lat,
                    lon=parsed_apartment.lon,
                    images_count=len(parsed_apartment.images_list),
                    # TODO: Need to implement
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
