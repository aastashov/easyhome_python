import graphene
from graphene import ObjectType, Schema, relay
from graphene_django.filter import DjangoFilterConnectionField

from hsearch.graph_ql.filters import OrderedDjangoFilterConnectionField
from hsearch.graph_ql.schema import ApartmentNode, ImageNode


class Query(ObjectType):
    apartment = relay.Node.Field(ApartmentNode)
    all_apartments = OrderedDjangoFilterConnectionField(ApartmentNode, orderBy=graphene.List(of_type=graphene.String))

    image = relay.Node.Field(ImageNode)
    all_images = DjangoFilterConnectionField(ImageNode)


schema = Schema(query=Query)
