from __future__ import annotations

from http import HTTPStatus

import pytest

from tests.easyhome.factories import ApartmentFactory

pytestmark = pytest.mark.django_db


def test_all_apartments_query(client_query: callable) -> None:
    # Given: a list of apartments
    apartments = ApartmentFactory.create_batch(size=10)

    query = """
        query {
          allApartments {
              edges {
                node {
                  externalId
                  url
                }
              }
            }
          }
        """

    # When: the query is executed
    response = client_query(query)

    # Then: the response should contain the list of apartments
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "data": {
            "allApartments": {
                "edges": [
                    {"node": {"externalId": apartment.external_id, "url": apartment.url}}
                    for apartment in apartments
                ],
            },
        },
    }
