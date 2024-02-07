from __future__ import annotations  # noqa: D100

from typing import Any

from django.core.management import BaseCommand, CommandParser

from easyhome.parser.http_client import HttpClient
from easyhome.parser.services import ParseSiteService
from easyhome.parser.sites.diesel import Diesel
from easyhome.parser.sites.lalafo import Lalafo


class Command(BaseCommand):  # noqa: D101
    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401, D107
        super().__init__(*args, **kwargs)

        self.sites = {
            "lalafo": Lalafo(),
            "diesel": Diesel(),
        }

    def add_arguments(self, parser: CommandParser) -> None:  # noqa: D102
        parser.add_argument("--site")

    def handle(self, *args: Any, **options: Any) -> str | None:  # noqa: ANN401, D102
        site = options["site"]
        site_parser = self.sites.get(site)
        if not site_parser:
            self.stdout.write(f"The site {site} not found.")
            return

        use_case = ParseSiteService(http_client=HttpClient(), site=site_parser)
        use_case.parse()
        return None
