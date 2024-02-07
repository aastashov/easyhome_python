from __future__ import annotations  # noqa: D100


def yes_no_img(variable: bool) -> str:  # noqa: FBT001
    """Use this function to display a boolean value as an image in the admin panel."""
    res = ("yes", "True") if variable else ("no", "False")
    return '<img src="/static/admin/img/icon-{}.svg" alt="{}">'.format(*res)
