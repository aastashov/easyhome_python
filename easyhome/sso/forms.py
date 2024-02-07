from __future__ import annotations  # noqa: D100

from captcha.fields import ReCaptchaField
from django.contrib.admin.forms import AdminAuthenticationForm as _AdminAuthenticationForm


class AdminAuthenticationForm(_AdminAuthenticationForm):  # noqa: D101
    captcha = ReCaptchaField()
