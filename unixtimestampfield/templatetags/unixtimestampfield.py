"""
UnixTimeStampField template tags.

release |release|, version |version|


.. versionadded:: 0.3.4

    Add extra function param

.. versionadded:: 0.3.3

    Initial


Contents
--------

Functions:

* :func:`to_datetime`
* :func:`to_timestamp`

Members
-------

"""
from __future__ import annotations

import time

from django.conf import settings
from django.template import Library
from django.utils import timezone
from pytz import utc

register = Library()


@register.filter("to_datetime")
def to_datetime(field):
    try:
        if type(field) in (float, str):
            field = timezone.datetime.fromtimestamp(field, utc)
            if settings.USE_TZ:
                field = timezone.localtime(field, timezone.get_default_timezone())
        return field
    except:
        return ""


@register.filter("to_timestamp")
def to_timestamp(field):
    try:
        if type(field) == timezone.datetime:
            if settings.USE_TZ and timezone.is_aware(field):
                field = timezone.localtime(field, utc)
            # Py2 doesn't supports timestamp()
            if hasattr(field, "timestamp"):
                return field.timestamp()
            return time.mktime(field.timetuple()) + field.microsecond * 0.00001

        return field
    except:
        return ""
