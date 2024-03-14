from __future__ import annotations

from graphene import relay
from graphene_django import DjangoObjectType

from easyhome.easyhome.models import Apartment, Image
from easyhome.graph_ql.filters import ApartmentFilter, ImageFilter


class ApartmentNode(DjangoObjectType):
    """Use this class to define the ApartmentNode."""

    class Meta:
        """Metaclass for the ApartmentNode."""

        model = Apartment
        filterset_class = ApartmentFilter
        interfaces = (relay.Node,)


class ImageNode(DjangoObjectType):
    """Use this class to define the ImageNode."""

    class Meta:
        """Metaclass for the ImageNode."""

        model = Image
        filterset_class = ImageFilter
        interfaces = (relay.Node,)
