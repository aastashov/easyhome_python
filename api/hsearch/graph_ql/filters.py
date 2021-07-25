import django_filters
from graphene import DateTime
from graphene.utils.str_converters import to_snake_case
from graphene_django.converter import convert_django_field
from graphene_django.filter import DjangoFilterConnectionField
from unixtimestampfield import UnixTimeStampField

from hsearch.models import Apartment, Image


@convert_django_field.register(UnixTimeStampField)
def convert_field_to_string(field, registry=None):
    return DateTime(description=field.help_text, required=not field.null)


class OrderedDjangoFilterConnectionField(DjangoFilterConnectionField):
    @classmethod
    def resolve_queryset(cls, connection, iterable, info, args, filtering_args, filterset_class):
        qs = super().resolve_queryset(connection, iterable, info, args, filtering_args, filterset_class)
        order = args.get("orderBy", None)
        if order:
            snake_order = to_snake_case(order) if isinstance(order, str) else [to_snake_case(o) for o in order]
            qs = qs.order_by(*snake_order).distinct()
        return qs


class ApartmentFilter(django_filters.FilterSet):
    created = django_filters.DateTimeFilter()

    topic = django_filters.CharFilter(lookup_expr="icontains")
    body = django_filters.CharFilter(lookup_expr="icontains")

    rooms = django_filters.Filter(method="filter_range")
    area = django_filters.Filter(method="filter_range")
    floor = django_filters.Filter(method="filter_range")
    price = django_filters.Filter(method="filter_range")

    with_images = django_filters.BooleanFilter(method="filter_with_images")

    @staticmethod
    def filter_range(queryset, name, value: str):
        if len(value.split(",")) == 2:
            price_from, price_to = value.split(",")  # type: str, str
            if price_from.isdigit() and price_to.isdigit():
                return queryset.filter(**{f"{name}__range": [price_from, price_to]})
            if price_from.isdigit() and price_to == "":
                return queryset.filter(**{f"{name}__gte": price_from})
            if price_to.isdigit() and price_from == "":
                return queryset.filter(**{f"{name}__lte": price_to})
        elif value.isdigit():
            return queryset.filter(**{name: value})
        return queryset.none()

    @staticmethod
    def filter_with_images(queryset, name, value: bool):
        if value:
            return queryset.filter(images_count__gt=0)
        return queryset.filter(images_count__lt=1)

    class Meta:
        model = Apartment
        fields = [
            "id",
            "url",
            "topic",
            "phone",
            "rooms",
            "body",
            "images_count",
            "price",
            "currency",
            "area",
            "city",
            "room_type",
            "site",
            "floor",
            "max_floor",
            "district",
            "lat",
            "lon",
            "created",
        ]


class ImageFilter(django_filters.FilterSet):
    created = django_filters.DateTimeFilter()

    class Meta:
        model = Image
        fields = [
            "id",
            "apartment",
            "path",
            "created",
        ]
