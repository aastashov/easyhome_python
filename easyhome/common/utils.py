from __future__ import annotations  # noqa: D100


class Singleton:  # noqa: D101
    def __new__(cls, *args: list[str], **kwargs: dict[str, str]):  # noqa: ANN204, D102
        it = cls.__dict__.get("__it__", None)
        if it is not None:
            return it

        cls.__it__ = it = object.__new__(cls)
        it._init(*args, **kwargs)  # noqa: SLF001
        return it

    def _init(self, *args: list[str], **kwargs: dict[str, str]) -> None:
        pass
