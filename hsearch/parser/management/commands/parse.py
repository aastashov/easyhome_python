from typing import Any

from django.core.management import BaseCommand, CommandParser

from hsearch.parser.http_client import HttpClient
from hsearch.parser.services import ParseSiteService
from hsearch.parser.sites.diesel import Diesel
from hsearch.parser.sites.lalafo import Lalafo


class Command(BaseCommand):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.sites = {
            "lalafo": Lalafo(),
            "diesel": Diesel(),
        }

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--site")

    def handle(self, *args: Any, **options: Any) -> str | None:
        site = options["site"]
        site_parser = self.sites.get(site)
        if not site_parser:
            self.stdout.write(f"The site {site} not found.")
            return

        use_case = ParseSiteService(http_client=HttpClient(), site=site_parser)
        use_case.parse()
        return None
