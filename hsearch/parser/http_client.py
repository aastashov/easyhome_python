import asyncio
from http import HTTPStatus
from itertools import cycle

import aiohttp
from aiohttp_retry import ExponentialRetry, RetryClient
from bs4 import BeautifulSoup
from django.conf import settings
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from hsearch.common.utils import Singleton

# https://deviceatlas.com/blog/list-of-user-agent-strings
user_agent_list = [
    (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    ),
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    (
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36,gzip(gfe)"
    ),
]

user_agent_cycle = cycle(user_agent_list)


def get_session() -> Session:
    """
    Use this function to get the http session, with retry settings to be used the HubSpot API.

    For example, if the total=6 and backoff_factor is set to:
    1 second the successive sleeps will be 0.5, 1, 2, 4, 8, 16.
    2 seconds - 1, 2, 4, 8, 16, 32.
    10 seconds - 5, 10, 20, 40, 80, 160.

    :return: Session
    """
    retries = Retry(
        total=3,
        backoff_factor=1,
        allowed_methods=["GET"],
        status_forcelist=[
            HTTPStatus.BAD_GATEWAY,
            HTTPStatus.SERVICE_UNAVAILABLE,
            HTTPStatus.GATEWAY_TIMEOUT,
        ],
        raise_on_status=False,  # without this option request raises MaxRetryError on 500s without returning response.
    )
    adapter = HTTPAdapter(max_retries=retries)

    http = Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    return http


retry_options = ExponentialRetry(
    attempts=3,
    start_timeout=0.3,
    statuses={
        HTTPStatus.BAD_GATEWAY,
        HTTPStatus.SERVICE_UNAVAILABLE,
        HTTPStatus.GATEWAY_TIMEOUT,
    },
)


def get_retry_client() -> RetryClient:
    return RetryClient(raise_for_status=False, retry_options=retry_options)


class HttpClient(Singleton):
    """
    Returns a HttpClient to make requests to sites.

    Example:
    -------
        from hsearch.parser.http_client import HttpClient

        http_client = HttpClient()  # used default get_session()
        http_client = HttpClient(session=Session())  # you can pass your session
    """

    session: Session

    def _init(self, session: Session | None = None, *args: list[str], **kwargs: dict[str, str]) -> None:
        self.session = session or get_session()

    def _get_headers(self) -> dict[str, str]:
        return {"User-Agent": next(user_agent_cycle)}

    def fetch_first_page(self, page_url: str) -> BeautifulSoup:
        http_response = self.session.get(page_url, headers=self._get_headers())
        http_response.raise_for_status()

        return BeautifulSoup(http_response.content, "html.parser")

    async def _async_api_get(
        self,
        async_session: aiohttp.ClientSession | RetryClient,
        url: str,
        rid: int,
    ) -> tuple[int, str]:
        """Async request to GET data."""
        semaphore = asyncio.Semaphore(settings.AIOHTTP_REQUEST_LIMIT)
        async with semaphore:
            async with async_session.get(url, headers=self._get_headers()) as resp:
                if resp.status != 200:
                    raise Exception(f"Response {resp.status}.")
                return rid, await resp.text()

    async def _async_fetch_announcement_pages(self, pages_map: dict[int, str]) -> dict[int, str]:
        async with get_retry_client() as session:
            tasks = (
                asyncio.ensure_future(self._async_api_get(session, url, rid=_id)) for _id, url in pages_map.items()
            )
            result = await asyncio.gather(*tasks)
        return dict(result)

    def fetch_announcement_pages(
        self,
        pages_map: dict[int, str],
    ) -> dict[int, BeautifulSoup]:
        announcement_pages: dict[int, BeautifulSoup] = {}
        for external_id, context in asyncio.run(self._async_fetch_announcement_pages(pages_map)).items():
            announcement_pages[external_id] = BeautifulSoup(context, "html.parser")
        return announcement_pages
