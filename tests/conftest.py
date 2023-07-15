from collections.abc import Callable

import pytest
from bs4 import BeautifulSoup
from django.conf import settings


@pytest.fixture
def parser_datasets() -> Callable[[str], BeautifulSoup]:
    dataset_path = settings.BASE_DIR / "tests/parser/__dataset__"

    def wrap(file_path: str) -> BeautifulSoup:
        with (dataset_path / file_path).open(mode="r") as _f:
            parsed_file = BeautifulSoup(_f, "html.parser")
        return parsed_file

    return wrap
