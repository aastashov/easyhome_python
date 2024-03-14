"""Use this module to define the factories for the easyhome module."""
from __future__ import annotations

import factory
from faker import Faker

from easyhome.easyhome.models import Apartment

fake = Faker()
Faker.seed(0)


class ApartmentFactory(factory.django.DjangoModelFactory):
    external_id = factory.Sequence(lambda n: n)
    url = factory.Sequence(lambda n: f"https://ex.co/{n}")

    class Meta:
        """Use this class to define the metadata for the factory."""

        model = Apartment
