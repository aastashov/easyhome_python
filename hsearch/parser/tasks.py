from celery import shared_task

from hsearch.parser.http_client import HttpClient
from hsearch.parser.sites.lalafo import Lalafo
from hsearch.parser.usecase import ParseSiteUseCase


@shared_task(bind=True)
def parse_lalafo(self) -> None:
    use_case = ParseSiteUseCase(http_client=HttpClient(), site=Lalafo())
    use_case.parse()
