from datetime import datetime

from ninja import Schema
from pydantic import validator

from hsearch.hsearch.models import Currency


class ApartmentResponse(Schema):
    topic: str
    url: str

    price: int
    currency: Currency

    created_at: int
    modified_at: int
    deleted_at: int | None

    @validator("created_at", "modified_at", "deleted_at", pre=True)
    def convert_datetime_to_timestamp(cls, value: datetime | int | None) -> int:
        """
        Convert a datetime object or integer timestamp to a Unix timestamp.

        :param value: The value to convert. It can be a datetime object or an integer timestamp.
        :type value: datetime | int
        :return: The Unix timestamp representing the input value.
        :rtype: int
        :raises ValidationError: If the input value is not a datetime object or an integer.
        """
        if isinstance(value, datetime):
            return int(value.timestamp())
        return value
