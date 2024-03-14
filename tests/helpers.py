from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.test.utils import CaptureQueriesContext


def print_queries(queries: CaptureQueriesContext) -> str:
    """Return captured queries as a string."""
    return "\n" + "\n\n".join(map(lambda q: q["sql"], queries.captured_queries))  # noqa: C417
