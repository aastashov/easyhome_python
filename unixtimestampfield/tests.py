from __future__ import annotations

import logging

from django import forms
from django.core import exceptions
from django.db import models
from django.template import Context, Template
from django.test import TestCase, override_settings
from django.utils import timezone

from .fields import OrdinalField, OrdinalPatchMixin, TimestampPatchMixin, UnixTimeStampField

unix_0 = timezone.datetime(1970, 1, 1)
unix_0_utc = timezone.datetime(1970, 1, 1, tzinfo=timezone.utc)

ordinal_1 = timezone.datetime.fromordinal(1)
ordinal_1_utc = timezone.make_aware(timezone.datetime.fromordinal(1), timezone.utc)

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class MixinTest(TestCase):

    zero_utc = timezone.datetime(1970, 1, 1, 0, 0,  tzinfo=timezone.utc)
    oneyear_utc = timezone.datetime(
        1971, 1, 1, 1, 1, 1, 123400, tzinfo=timezone.utc)  # 31539661.123400
    oneyear_utc_i = timezone.datetime(1971, 1, 1, 1, 1, 1,  tzinfo=timezone.utc)  # 31539661.0
    zero = timezone.datetime(1970, 1, 1, 0, 0)
    oneyear = timezone.datetime(1971, 1, 1, 1, 1, 1, 123400)
    oneyear_i = timezone.datetime(1971, 1, 1, 1, 1, 1)
    negyear_utc = timezone.datetime(
        1969, 1, 1, 1, 1, 1, 123400, tzinfo=timezone.utc)  # -31532338.8766
    negyear_utc_i = timezone.datetime(1969, 1, 1, 1, 1, 1, tzinfo=timezone.utc)  # -31532339

    @override_settings(USE_TZ=True, TIME_ZONE="UTC")
    def test_to_timestamp_utc(self) -> None:
        ts = TimestampPatchMixin()

        assert ts.to_timestamp(self.zero_utc) == 0
        assert ts.to_timestamp(self.oneyear_utc) == 31539661.1234
        assert ts.to_timestamp(self.oneyear_utc_i) == 31539661
        assert ts.to_timestamp(self.negyear_utc) == -31532338.8766
        assert ts.to_timestamp(self.negyear_utc_i) == -31532339

    @override_settings(USE_TZ=True, TIME_ZONE="Asia/Taipei")
    def test_to_timestamp_with_tz(self) -> None:
        ts = TimestampPatchMixin()

        assert ts.to_timestamp(timezone.localtime(self.zero_utc)) == 0
        assert ts.to_timestamp(timezone.localtime(self.oneyear_utc)) == 31539661.1234
        assert ts.to_timestamp(timezone.localtime(self.oneyear_utc_i)) == 31539661
        assert ts.to_timestamp(timezone.localtime(self.negyear_utc)) == -31532338.8766
        assert ts.to_timestamp(timezone.localtime(self.negyear_utc_i)) == -31532339

    @override_settings(USE_TZ=False)
    def test_to_timestamp_without_tz(self) -> None:
        ts = TimestampPatchMixin()

        assert ts.to_timestamp(self.zero_utc) == 0
        assert ts.to_timestamp(self.zero) == 0
        assert ts.to_timestamp(timezone.localtime(self.zero_utc)) == 0
        assert ts.to_timestamp(self.oneyear) == 31539661.1234
        assert ts.to_timestamp(self.oneyear_utc) == 31539661.1234
        assert ts.to_timestamp(self.oneyear_utc_i) == 31539661
        assert ts.to_timestamp(self.negyear_utc) == -31532338.8766
        assert ts.to_timestamp(self.negyear_utc_i) == -31532339

    @override_settings(USE_TZ=True, TIME_ZONE="UTC")
    def test_to_naive_utc(self) -> None:
        ts = TimestampPatchMixin()

        assert self.zero == ts.to_naive_datetime(0)
        assert self.zero == ts.to_naive_datetime(0.0)
        assert self.zero == ts.to_naive_datetime("0")
        assert self.zero == ts.to_naive_datetime("1970-01-01 00:00:00")

        assert self.oneyear_i == ts.to_naive_datetime(31539661)
        assert self.oneyear == ts.to_naive_datetime(31539661.1234)
        assert self.oneyear == ts.to_naive_datetime("31539661.123400")
        assert self.oneyear == ts.to_naive_datetime("1971-01-01 01:01:01.123400")

    @override_settings(USE_TZ=True, TIME_ZONE="Asia/Taipei")
    def test_to_naive_with_tz(self) -> None:
        ts = TimestampPatchMixin()

        assert self.zero == ts.to_naive_datetime(0)
        assert self.zero == ts.to_naive_datetime(0.0)
        assert self.zero == ts.to_naive_datetime("0")
        assert self.zero == ts.to_naive_datetime("1970-01-01 00:00:00")

        assert self.oneyear_i == ts.to_naive_datetime(31539661)
        assert self.oneyear == ts.to_naive_datetime(31539661.1234)
        assert self.oneyear == ts.to_naive_datetime("31539661.123400")
        assert self.oneyear == ts.to_naive_datetime("1971-01-01 01:01:01.123400")

    @override_settings(USE_TZ=False)
    def test_to_naive_without_tz(self) -> None:
        ts = TimestampPatchMixin()

        assert self.zero == ts.to_naive_datetime(0)
        assert self.zero == ts.to_naive_datetime(0.0)
        assert self.zero == ts.to_naive_datetime("0")
        assert self.zero == ts.to_naive_datetime("1970-01-01 00:00:00")

        assert self.oneyear_i == ts.to_naive_datetime(31539661)
        assert self.oneyear == ts.to_naive_datetime(31539661.1234)
        assert self.oneyear == ts.to_naive_datetime("31539661.123400")
        assert self.oneyear == ts.to_naive_datetime("1971-01-01 01:01:01.123400")

    @override_settings(USE_TZ=True, TIME_ZONE="UTC")
    def test_to_utc_utc(self) -> None:
        ts = TimestampPatchMixin()

        assert self.zero_utc == ts.to_utc_datetime(0)
        assert self.zero_utc == ts.to_utc_datetime(0.0)
        assert self.zero_utc == ts.to_utc_datetime("0")
        assert self.zero_utc == ts.to_utc_datetime("1970-01-01 00:00:00")

        assert self.oneyear_utc_i == ts.to_utc_datetime(31539661)
        assert self.oneyear_utc == ts.to_utc_datetime(31539661.1234)
        assert self.oneyear_utc == ts.to_utc_datetime("31539661.123400")
        assert self.oneyear_utc == ts.to_utc_datetime("1971-01-01 01:01:01.123400")

    @override_settings(USE_TZ=True, TIME_ZONE="Asia/Taipei")
    def test_to_utc_with_tz(self) -> None:
        ts = TimestampPatchMixin()

        assert self.zero_utc == ts.to_utc_datetime(0)
        assert self.zero_utc == ts.to_utc_datetime(0.0)
        assert self.zero_utc == ts.to_utc_datetime("0")
        assert self.zero_utc == ts.to_utc_datetime("1970-01-01 00:00:00")

        assert self.oneyear_utc_i == ts.to_utc_datetime(31539661)
        assert self.oneyear_utc == ts.to_utc_datetime(31539661.1234)
        assert self.oneyear_utc == ts.to_utc_datetime("31539661.123400")
        assert self.oneyear_utc == ts.to_utc_datetime("1971-01-01 01:01:01.123400")

    @override_settings(USE_TZ=False)
    def test_to_utc_without_tz(self) -> None:
        ts = TimestampPatchMixin()

        assert self.zero_utc == ts.to_utc_datetime(0)
        assert self.zero_utc == ts.to_utc_datetime(0.0)
        assert self.zero_utc == ts.to_utc_datetime("0")
        assert self.zero_utc == ts.to_utc_datetime("1970-01-01 00:00:00")

        assert self.oneyear_utc_i == ts.to_utc_datetime(31539661)
        assert self.oneyear_utc == ts.to_utc_datetime(31539661.1234)
        assert self.oneyear_utc == ts.to_utc_datetime("31539661.123400")
        assert self.oneyear_utc == ts.to_utc_datetime("1971-01-01 01:01:01.123400")

    @override_settings(USE_TZ=True, TIME_ZONE="UTC")
    def test_to_datetime_utc(self) -> None:
        ts = TimestampPatchMixin()

        assert self.zero_utc == ts.to_datetime(0)
        assert self.zero_utc == ts.to_datetime(0.0)
        assert self.zero_utc == ts.to_datetime("0")
        assert self.zero_utc == ts.to_datetime("1970-01-01 00:00:00")

        assert self.oneyear_utc_i == ts.to_datetime(31539661)
        assert self.oneyear_utc == ts.to_datetime(31539661.1234)
        assert self.oneyear_utc == ts.to_datetime("31539661.123400")
        assert self.oneyear_utc == ts.to_datetime("1971-01-01 01:01:01.123400")

    @override_settings(USE_TZ=True, TIME_ZONE="Asia/Taipei")
    def test_to_datetime_with_tz(self) -> None:
        ts = TimestampPatchMixin()
        zero = timezone.localtime(self.zero_utc)
        oneyear = timezone.localtime(self.oneyear_utc)
        oneyear_i = timezone.localtime(self.oneyear_utc_i)

        assert zero == ts.to_datetime(0)
        assert zero == ts.to_datetime(0.0)
        assert zero == ts.to_datetime("0")
        assert zero == ts.to_datetime("1970-01-01 00:00:00")

        assert oneyear_i == ts.to_datetime(31539661)
        assert oneyear == ts.to_datetime(31539661.1234)
        assert oneyear == ts.to_datetime("31539661.123400")
        assert oneyear == ts.to_datetime("1971-01-01 01:01:01.123400")

    @override_settings(USE_TZ=False)
    def test_to_datetime_without_tz(self) -> None:
        ts = TimestampPatchMixin()

        assert self.zero == ts.to_datetime(0)
        assert self.zero == ts.to_datetime(0.0)
        assert self.zero == ts.to_datetime("0")
        assert self.zero == ts.to_datetime("1970-01-01 00:00:00")

        assert self.oneyear_i == ts.to_datetime(31539661)
        assert self.oneyear == ts.to_datetime(31539661.1234)
        assert self.oneyear == ts.to_datetime("31539661.123400")
        assert self.oneyear == ts.to_datetime("1971-01-01 01:01:01.123400")

    @override_settings(USE_TZ=True, TIME_ZONE="UTC")
    def test_over_and_under_flow(self) -> None:
        ts = TimestampPatchMixin()

        self.assertRaises(exceptions.ValidationError, ts.from_number, 253402272000)
        self.assertRaises(exceptions.ValidationError, ts.from_number, -719163)


class ForTestModel(models.Model):

    created = UnixTimeStampField(auto_now_add=True)
    modified = UnixTimeStampField(auto_now=True)
    str_ini = UnixTimeStampField(default="0.0")
    str_dt_ini = UnixTimeStampField(default="1970-01-01 00:00:00")
    float_ini = UnixTimeStampField(default=0.0)
    int_ini = UnixTimeStampField(default=0.0)
    dt_ini = UnixTimeStampField(default=unix_0_utc)

    use_numeric_field = UnixTimeStampField(use_numeric=True, default=0.0)
    round_3_field = UnixTimeStampField(use_numeric=True, round_to=3, default=0.0)


class TimeStampFieldTest(TestCase):

    @override_settings(USE_TZ=True, TIME_ZONE="UTC")
    def test_init_with_use_tz(self) -> None:
        now = timezone.now()
        expected = timezone.datetime(1970, 1, 1, tzinfo=timezone.utc)
        t = ForTestModel.objects.create()

        assert t.created > now
        assert t.modified > now
        assert t.str_ini == expected
        assert t.str_dt_ini == expected
        assert t.float_ini == expected
        assert t.int_ini == expected

    @override_settings(USE_TZ=True, TIME_ZONE="UTC")
    def test_assignment_with_tz(self) -> None:
        expected = timezone.datetime(1970, 1, 1, 0, 0, 3, tzinfo=timezone.utc)
        t = ForTestModel.objects.create()

        pre_modified = t.modified

        t.str_ini = "3"
        t.str_dt_ini = "1970-01-01 00:00:03"
        t.float_ini = 3.0
        t.int_ini = 3
        t.dt_ini = timezone.datetime(1970, 1, 1, 0, 0, 3, tzinfo=timezone.utc)
        t.use_numeric_field = 3.1111116
        t.round_3_field = 3.1116
        t.save()

        if hasattr(t, "refresh_from_db"):
            t.refresh_from_db()
        else:
            t = ForTestModel.objects.get(id=t.id)

        assert t.modified > pre_modified
        assert t.str_ini == expected
        assert t.str_dt_ini == expected
        assert t.float_ini == expected
        assert t.int_ini == expected
        assert t.use_numeric_field == 3.111112
        assert t.round_3_field == 3.112

    @override_settings(USE_TZ=True, TIME_ZONE="Asia/Taipei")
    def test_init_with_different_tz(self) -> None:
        now = timezone.now()
        expected = timezone.localtime(
            timezone.datetime(1970, 1, 1, tzinfo=timezone.utc),
            timezone.pytz.timezone("Asia/Taipei"),
        )
        t = ForTestModel.objects.create()

        assert t.created > now
        assert t.modified > now
        assert t.str_ini == expected
        assert t.str_dt_ini == expected
        assert t.float_ini == expected
        assert t.int_ini == expected

    @override_settings(USE_TZ=True, TIME_ZONE="Asia/Taipei")
    def test_assignment_with_different_tz(self) -> None:
        expected = timezone.localtime(
            timezone.datetime(1970, 1, 1, 0, 0, 3, tzinfo=timezone.utc),
            timezone.pytz.timezone("Asia/Taipei"),
        )

        t = ForTestModel.objects.create()

        pre_modified = t.modified

        t.str_ini = "3"
        t.str_dt_ini = "1970-01-01 00:00:03"
        t.float_ini = 3.0
        t.int_ini = 3
        t.dt_ini = timezone.datetime.fromtimestamp(3.0, timezone.pytz.timezone("Asia/Taipei"))
        t.use_numeric_field = 3.1111116
        t.round_3_field = 3.1116
        t.save()

        if hasattr(t, "refresh_from_db"):
            t.refresh_from_db()
        else:
            t = ForTestModel.objects.get(id=t.id)

        assert t.modified > pre_modified
        assert t.str_ini == expected
        assert t.str_dt_ini == expected
        assert t.float_ini == expected
        assert t.int_ini == expected
        assert t.use_numeric_field == 3.111112
        assert t.round_3_field == 3.112

    @override_settings(USE_TZ=False)
    def test_init_without_tz(self) -> None:
        now = timezone.datetime.utcnow()
        expected = timezone.datetime(1970, 1, 1, 0, 0)
        t = ForTestModel.objects.create()

        assert t.created > now
        assert t.modified > now
        assert t.str_ini == expected
        assert t.str_dt_ini == expected
        assert t.float_ini == expected
        assert t.int_ini == expected

    @override_settings(USE_TZ=False)
    def test_assignment_without_tz(self) -> None:
        expected = timezone.datetime(1970, 1, 1, 0, 0, 3)
        t = ForTestModel.objects.create()

        pre_modified = t.modified

        t.str_ini = "3"
        t.str_dt_ini = "1970-01-01 00:00:03"
        t.float_ini = 3.0
        t.int_ini = 3
        t.dt_ini = timezone.datetime.fromtimestamp(3.0)
        t.save()

        if hasattr(t, "refresh_from_db"):
            t.refresh_from_db()
        else:
            t = ForTestModel.objects.get(id=t.id)

        assert t.modified > pre_modified
        assert t.str_ini == expected
        assert t.str_dt_ini == expected
        assert t.float_ini == expected
        assert t.int_ini == expected

    @override_settings(USE_TZ=False)
    def test_assignment_with_big_num(self) -> None:
        expected = timezone.datetime(1970, 1, 1, 0, 0) + timezone.timedelta(seconds=14248491461)
        t = ForTestModel.objects.create()

        pre_modified = t.modified

        t.str_ini = "14248491461"
        t.float_ini = 14248491461.0
        t.int_ini = 14248491461
        t.dt_ini = timezone.datetime.fromtimestamp(14248491461.0)
        t.save()

        if hasattr(t, "refresh_from_db"):
            t.refresh_from_db()
        else:
            t = ForTestModel.objects.get(id=t.id)

        assert t.modified > pre_modified
        assert t.str_ini == expected
        assert t.float_ini == expected
        assert t.int_ini == expected

    @override_settings(USE_TZ=False)
    def test_assignment_overflow(self) -> None:

        t = ForTestModel.objects.create()
        t.float_ini = 14248491461222.0

        self.assertRaises(exceptions.ValidationError, t.save)


class ForTestModelForm(forms.ModelForm):

    class Meta:
        model = ForTestModel
        fields = ["str_ini", "float_ini", "int_ini", "dt_ini",
                  "use_numeric_field", "round_3_field"]


class FormFieldTest(TestCase):

    def test_noraml(self) -> None:
        data = {
            "str_ini": "1999-12-11 10:23:13",
            "float_ini": 3.0,
            "int_ini": 3,
            "dt_ini": 3,
            "use_numeric_field": 0,
            "round_3_field": 0,
        }

        tform = ForTestModelForm(data=data)

        assert tform.is_valid()

    def test_empty_form(self) -> None:

        data = {}

        tform = ForTestModelForm(data=data)

        assert not tform.is_valid()
        errors = {"dt_ini": ["This field is required."],
                  "float_ini": ["This field is required."],
                  "int_ini": ["This field is required."],
                  "round_3_field": ["This field is required."],
                  "str_ini": ["This field is required."],
                  "use_numeric_field": ["This field is required."]}
        self.assertDictEqual(tform.errors, errors)
        assert tform.error_class == forms.utils.ErrorList

    def test_partial_data(self) -> None:

        data = {
            "int_ini": 0,
            "round_3_field": 0,
            "str_ini": "3",
        }

        tform = ForTestModelForm(data=data)

        assert not tform.is_valid()
        errors = {"dt_ini": ["This field is required."],
                  "float_ini": ["This field is required."],
                  "use_numeric_field": ["This field is required."]}
        self.assertDictEqual(tform.errors, errors)
        assert tform.error_class == forms.utils.ErrorList

    def test_invalid_data(self) -> None:

        data = {
            "str_ini": ["hello"],
            "float_ini": 3.0,
            "int_ini": 3,
            "dt_ini": 3,
            "use_numeric_field": 0,
            "round_3_field": 0,
        }

        tform = ForTestModelForm(data=data)

        assert not tform.is_valid()
        errors = {"str_ini": ["Unable to convert value: '['hello']' to datetime"
                              ", please use 'YYYY-mm-dd HH:MM:SS'"]}
        self.assertDictEqual(tform.errors, errors)
        assert tform.error_class == forms.utils.ErrorList


class OrdMixinTest(TestCase):

    zero_utc = timezone.datetime(1, 1, 1, 0, 0,  tzinfo=timezone.utc)
    oneyear_utc = timezone.datetime(1, 12, 31, 0, 0, tzinfo=timezone.utc)  # 365
    zero = timezone.datetime(1, 1, 1, 0, 0)
    oneyear = timezone.datetime(1, 12, 31, 0, 0)  # 365

    @override_settings(USE_TZ=True, TIME_ZONE="UTC")
    def test_to_timestamp_utc(self) -> None:
        ts = OrdinalPatchMixin()

        assert ts.to_timestamp(self.zero_utc) == 1
        assert ts.to_timestamp(self.oneyear_utc) == 365

    @override_settings(USE_TZ=True, TIME_ZONE="Asia/Taipei")
    def test_to_timestamp_with_tz(self) -> None:
        ts = OrdinalPatchMixin()

        assert ts.to_timestamp(timezone.localtime(self.zero_utc)) == 1
        assert ts.to_timestamp(timezone.localtime(self.oneyear_utc)) == 365

    @override_settings(USE_TZ=False)
    def test_to_timestamp_without_tz(self) -> None:
        ts = OrdinalPatchMixin()

        assert ts.to_timestamp(self.zero_utc) == 1
        assert ts.to_timestamp(self.zero) == 1
        assert ts.to_timestamp(self.oneyear) == 365

    @override_settings(USE_TZ=True, TIME_ZONE="UTC")
    def test_to_naive_utc(self) -> None:
        ts = OrdinalPatchMixin()

        assert self.zero == ts.to_naive_datetime(1)
        assert self.zero == ts.to_naive_datetime(1.0)
        assert self.zero == ts.to_naive_datetime("1")
        assert self.zero == ts.to_naive_datetime("0001-01-01 00:00:00")

        assert self.oneyear == ts.to_naive_datetime(365)
        assert self.oneyear == ts.to_naive_datetime(365.0)
        assert self.oneyear == ts.to_naive_datetime("365")
        assert self.oneyear == ts.to_naive_datetime("0001-12-31 00:00:00")

    @override_settings(USE_TZ=True, TIME_ZONE="Asia/Taipei")
    def test_to_naive_with_tz(self) -> None:
        ts = OrdinalPatchMixin()

        assert self.zero == ts.to_naive_datetime(1)
        assert self.zero == ts.to_naive_datetime(1.0)
        assert self.zero == ts.to_naive_datetime("1")
        assert self.zero == ts.to_naive_datetime("0001-01-01 00:00:00")

        assert self.oneyear == ts.to_naive_datetime(365)
        assert self.oneyear == ts.to_naive_datetime(365.0)
        assert self.oneyear == ts.to_naive_datetime("365")
        assert self.oneyear == ts.to_naive_datetime("0001-12-31 00:00:00")

    @override_settings(USE_TZ=False)
    def test_to_naive_without_tz(self) -> None:
        ts = OrdinalPatchMixin()

        assert self.zero == ts.to_naive_datetime(1)
        assert self.zero == ts.to_naive_datetime(1.0)
        assert self.zero == ts.to_naive_datetime("1")
        assert self.zero == ts.to_naive_datetime("0001-01-01 00:00:00")

        assert self.oneyear == ts.to_naive_datetime(365)
        assert self.oneyear == ts.to_naive_datetime(365.0)
        assert self.oneyear == ts.to_naive_datetime("365")
        assert self.oneyear == ts.to_naive_datetime("0001-12-31 00:00:00")

    @override_settings(USE_TZ=True, TIME_ZONE="UTC")
    def test_to_utc_utc(self) -> None:
        ts = OrdinalPatchMixin()

        assert self.zero_utc == ts.to_utc_datetime(1)
        assert self.zero_utc == ts.to_utc_datetime(1.0)
        assert self.zero_utc == ts.to_utc_datetime("1")
        assert self.zero_utc == ts.to_utc_datetime("0001-01-01 00:00:00")

        assert self.oneyear_utc == ts.to_utc_datetime(365)
        assert self.oneyear_utc == ts.to_utc_datetime(365.0)
        assert self.oneyear_utc == ts.to_utc_datetime("365")
        assert self.oneyear_utc == ts.to_utc_datetime("0001-12-31 00:00:00")

    @override_settings(USE_TZ=True, TIME_ZONE="Asia/Taipei")
    def test_to_utc_with_tz(self) -> None:
        ts = OrdinalPatchMixin()

        assert self.zero_utc == ts.to_utc_datetime(1)
        assert self.zero_utc == ts.to_utc_datetime(1.0)
        assert self.zero_utc == ts.to_utc_datetime("1")
        assert self.zero_utc == ts.to_utc_datetime("0001-01-01 00:00:00")

        assert self.oneyear_utc == ts.to_utc_datetime(365)
        assert self.oneyear_utc == ts.to_utc_datetime(365.0)
        assert self.oneyear_utc == ts.to_utc_datetime("365")
        assert self.oneyear_utc == ts.to_utc_datetime("0001-12-31 00:00:00")

    @override_settings(USE_TZ=False)
    def test_to_utc_without_tz(self) -> None:
        ts = OrdinalPatchMixin()

        assert self.zero_utc == ts.to_utc_datetime(1)
        assert self.zero_utc == ts.to_utc_datetime(1.0)
        assert self.zero_utc == ts.to_utc_datetime("1")
        assert self.zero_utc == ts.to_utc_datetime("0001-01-01 00:00:00")

        assert self.oneyear_utc == ts.to_utc_datetime(365)
        assert self.oneyear_utc == ts.to_utc_datetime(365.0)
        assert self.oneyear_utc == ts.to_utc_datetime("365")
        assert self.oneyear_utc == ts.to_utc_datetime("0001-12-31 00:00:00")

    @override_settings(USE_TZ=True, TIME_ZONE="UTC")
    def test_to_datetime_utc(self) -> None:
        ts = OrdinalPatchMixin()

        assert self.zero_utc == ts.to_datetime(1)
        assert self.zero_utc == ts.to_datetime(1.0)
        assert self.zero_utc == ts.to_datetime("1")
        assert self.zero_utc == ts.to_datetime("0001-01-01 00:00:00")

        assert self.oneyear_utc == ts.to_datetime(365)
        assert self.oneyear_utc == ts.to_datetime(365.0)
        assert self.oneyear_utc == ts.to_datetime("365")
        assert self.oneyear_utc == ts.to_datetime("0001-12-31 00:00:00")

    @override_settings(USE_TZ=True, TIME_ZONE="Asia/Taipei")
    def test_to_datetime_with_tz(self) -> None:
        ts = OrdinalPatchMixin()
        zero = timezone.localtime(self.zero_utc)
        oneyear = timezone.localtime(self.oneyear_utc)

        assert zero == ts.to_datetime(1)
        assert zero == ts.to_datetime(1.0)
        assert zero == ts.to_datetime("1")
        assert zero == ts.to_datetime("0001-01-01 00:00:00")

        assert oneyear == ts.to_datetime(365)
        assert oneyear == ts.to_datetime(365.0)
        assert oneyear == ts.to_datetime("365")
        assert oneyear == ts.to_datetime("0001-12-31 00:00:00")

    @override_settings(USE_TZ=False)
    def test_to_datetime_without_tz(self) -> None:
        ts = OrdinalPatchMixin()

        assert self.zero == ts.to_datetime(1)
        assert self.zero == ts.to_datetime(1.0)
        assert self.zero == ts.to_datetime("1")
        assert self.zero == ts.to_datetime("0001-01-01 00:00:00")

        assert self.oneyear == ts.to_datetime(365)
        assert self.oneyear == ts.to_datetime(365.0)
        assert self.oneyear == ts.to_datetime("365")
        assert self.oneyear == ts.to_datetime("0001-12-31 00:00:00")

    @override_settings(USE_TZ=True, TIME_ZONE="UTC")
    def test_over_and_under_flow(self) -> None:
        ts = OrdinalPatchMixin()

        self.assertRaises(exceptions.ValidationError, ts.from_number, 3652060)
        self.assertRaises(exceptions.ValidationError, ts.from_number, 0)
        self.assertRaises(exceptions.ValidationError, ts.from_number, -1)


class ForOrdinalTestModel(models.Model):

    created = OrdinalField(auto_now_add=True)
    modified = OrdinalField(auto_now=True)
    str_ini = OrdinalField(default="1")
    float_ini = OrdinalField(default=1)
    int_ini = OrdinalField(default=1)
    dt_ini = OrdinalField(default=ordinal_1)


class OrdinalFieldTest(TestCase):

    @override_settings(USE_TZ=True, TIME_ZONE="UTC")
    def test_init_with_utc(self) -> None:
        today = timezone.make_aware(
            timezone.datetime.fromordinal(timezone.now().toordinal()), timezone.utc)
        expected = timezone.make_aware(timezone.datetime.fromordinal(1), timezone.utc)
        m = ForOrdinalTestModel.objects.create()

        assert m.created == today
        assert m.modified == today
        assert m.str_ini == expected
        assert m.float_ini == expected
        assert m.int_ini == expected
        assert m.dt_ini == expected

    @override_settings(USE_TZ=True, TIME_ZONE="UTC")
    def test_assignment_with_tz(self) -> None:
        today = timezone.make_aware(
            timezone.datetime.fromordinal(timezone.now().toordinal()), timezone.utc)
        expected = timezone.make_aware(timezone.datetime.fromordinal(3), timezone.utc)
        m = ForOrdinalTestModel.objects.create()

        m.str_ini = "3"
        m.float_ini = 3.0
        m.int_ini = 3
        m.dt_ini = timezone.make_aware(timezone.datetime.fromordinal(3), timezone.utc)
        m.save()

        if hasattr(m, "refresh_from_db"):
            m.refresh_from_db()
        else:
            m = ForOrdinalTestModel.objects.get(id=m.id)

        assert m.modified == today
        assert m.str_ini == expected
        assert m.float_ini == expected
        assert m.int_ini == expected

    @override_settings(USE_TZ=True, TIME_ZONE="Asia/Taipei")
    def test_init_with_different_tz(self) -> None:
        today = timezone.make_aware(
            timezone.datetime.fromordinal(timezone.now().toordinal()), timezone.utc)
        expected = timezone.localtime(
            timezone.make_aware(timezone.datetime.fromordinal(1), timezone.utc),
            timezone.pytz.timezone("Asia/Taipei"),
        )
        m = ForOrdinalTestModel.objects.create()

        assert m.created == today
        assert m.modified == today
        assert m.str_ini == expected
        assert m.float_ini == expected
        assert m.int_ini == expected

    @override_settings(USE_TZ=False)
    def test_init_without_tz(self) -> None:
        today = timezone.datetime.fromordinal(timezone.datetime.utcnow().toordinal())
        expected = timezone.datetime.fromordinal(1)
        m = ForOrdinalTestModel.objects.create()

        assert m.created == today
        assert m.modified == today
        assert m.str_ini == expected
        assert m.float_ini == expected
        assert m.int_ini == expected

    @override_settings(USE_TZ=False)
    def test_assignment_without_tz(self) -> None:

        today = timezone.datetime.fromordinal(timezone.datetime.utcnow().toordinal())
        expected = timezone.datetime.fromordinal(3)
        m = ForOrdinalTestModel.objects.create()

        m.str_ini = "3"
        m.float_ini = 3.0
        m.int_ini = 3
        m.dt_ini = timezone.datetime.fromordinal(3)
        m.save()

        if hasattr(m, "refresh_from_db"):
            m.refresh_from_db()
        else:
            m = ForOrdinalTestModel.objects.get(id=m.id)

        assert m.modified == today
        assert m.str_ini == expected
        assert m.float_ini == expected
        assert m.int_ini == expected

    @override_settings(USE_TZ=False)
    def test_assignment_overflow(self) -> None:

        t = ForOrdinalTestModel.objects.create()
        t.float_ini = 14248491461222.0

        self.assertRaises(exceptions.ValidationError, t.save)


class TemplateTagsTest(TestCase):

    def setUp(self) -> None:
        self.template = Template(
            "{% load unixtimestampfield %} "
            "{{t.str_ini|to_datetime}} "
            "{{t.str_ini|to_timestamp}}",
        )

    @override_settings(USE_TZ=True, TIME_ZONE="UTC")
    def test_render(self) -> None:
        t = ForTestModel()
        rendered = self.template.render(Context({"t": t}))
        assert "Jan. 1, 1970" in rendered
        assert "0.0" in rendered


class SubmiddlewareModel(models.Model):

    datetime = UnixTimeStampField(default=0.0)
    numeric = UnixTimeStampField(use_numeric=True, default=0.0)


class SubmiddlewareTest(TestCase):

    @override_settings(USE_TZ=True, TIME_ZONE="UTC")
    def test_default(self) -> None:
        t = SubmiddlewareModel.objects.create()
        expected = timezone.datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        if hasattr(t, "refresh_from_db"):
            t.refresh_from_db()
        else:
            t = ForTestModel.objects.get(id=t.id)

        assert t.datetime == expected
        assert t.numeric == 0

    @override_settings(USE_TZ=True, TIME_ZONE="UTC", USF_FORMAT="usf_datetime")
    def test_datetime(self) -> None:
        t = SubmiddlewareModel.objects.create()
        expected = timezone.datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        assert t.datetime == expected
        assert t.numeric == expected

    @override_settings(USE_TZ=True, TIME_ZONE="UTC", USF_FORMAT="usf_timestamp")
    def test_timestamp(self) -> None:
        t = SubmiddlewareModel.objects.create()

        assert t.datetime == 0
        assert t.numeric == 0

    @override_settings(USE_TZ=True, TIME_ZONE="UTC", USF_FORMAT="invalid")
    def test_invalid_option(self) -> None:
        t = SubmiddlewareModel.objects.create()
        expected = timezone.datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        if hasattr(t, "refresh_from_db"):
            t.refresh_from_db()
        else:
            t = ForTestModel.objects.get(id=t.id)

        assert t.datetime == expected
        assert t.numeric == 0
