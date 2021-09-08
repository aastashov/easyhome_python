from graphene import relay
from graphene_django import DjangoObjectType

from hsearch.graph_ql.connection import ExtendedConnection
from hsearch.graph_ql.filters import ApartmentFilter, ImageFilter
from hsearch.models import Apartment, Image


class ApartmentNode(DjangoObjectType):
    class Meta:
        model = Apartment
        filterset_class = ApartmentFilter
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(is_deleted=False)


class ImageNode(DjangoObjectType):
    class Meta:
        model = Image
        filterset_class = ImageFilter
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection
