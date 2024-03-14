from __future__ import annotations

from typing import Any, TYPE_CHECKING

import pytest
from bs4 import BeautifulSoup
from django.conf import settings
from graphene_django.utils.testing import graphql_query

if TYPE_CHECKING:
    from collections.abc import Callable

    from graphene.test import Client


@pytest.fixture  # noqa: PT001
def parser_datasets() -> Callable[[str], BeautifulSoup]:
    dataset_path = settings.BASE_DIR / "tests/parser/__dataset__"

    def wrap(file_path: str) -> BeautifulSoup:
        with (dataset_path / file_path).open(mode="r") as _f:
            parsed_file = BeautifulSoup(_f, "html.parser")
        return parsed_file  # noqa: RET504

    return wrap


@pytest.fixture()
def client_query(client: Client) -> Callable[..., dict]:
    def func(*args: list[Any], **kwargs: [dict[str, Any]]) -> dict[str, Any]:
        return graphql_query(*args, **kwargs, client=client, graphql_url="/graphql/")

    return func
