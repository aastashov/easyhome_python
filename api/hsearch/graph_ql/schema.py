from django.db.models import Count
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
        return (
            queryset.filter()
            .annotate(images_in_db=Count("images"))
            .filter(images_in_db__gt=0, is_deleted=False)
            .prefetch_related("images")
        )


class ImageNode(DjangoObjectType):
    class Meta:
        model = Image
        filterset_class = ImageFilter
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection
