from celery import shared_task

from hsearch.parser.http_client import HttpClient
from hsearch.parser.services import ParseSiteService
from hsearch.parser.sites.diesel import Diesel
from hsearch.parser.sites.lalafo import Lalafo


@shared_task(bind=True)
def parse_lalafo(self) -> None:
    use_case = ParseSiteService(http_client=HttpClient(), site=Lalafo())
    use_case.parse()


@shared_task(bind=True)
def parse_diesel(self) -> None:
    use_case = ParseSiteService(http_client=HttpClient(), site=Diesel())
    use_case.parse()
