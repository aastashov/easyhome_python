from __future__ import annotations

from graphene import ObjectType, Schema, relay
from graphene_django.filter import DjangoFilterConnectionField

from easyhome.graph_ql.schema import ApartmentNode, ImageNode


class Query(ObjectType):
    """Use this class to define the queries for the graphene schema."""

    apartment = relay.Node.Field(ApartmentNode)
    all_apartments = DjangoFilterConnectionField(ApartmentNode)

    image = relay.Node.Field(ImageNode)
    all_images = DjangoFilterConnectionField(ImageNode)


schema = Schema(query=Query)
