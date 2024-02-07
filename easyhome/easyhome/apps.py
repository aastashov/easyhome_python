"""EasyHome application configuration."""
from __future__ import annotations

from typing import TYPE_CHECKING

from apscheduler.triggers.interval import IntervalTrigger
from django.apps import AppConfig
from django.conf import settings

if TYPE_CHECKING:
    from apscheduler.schedulers.background import BackgroundScheduler


class EasyHomeConfig(AppConfig):
    """EasyHome application configuration."""

    name = "easyhome.easyhome"
    verbose_name = "EasyHome"

    def ready(self) -> None:
        """Run when the application is ready."""
        from easyhome.easyhome.dependencies import APP_CONTAINER

        APP_CONTAINER.config.from_dict(settings.__dict__["_wrapped"].__dict__)
        APP_CONTAINER.wire(
            modules=[
                __name__,
            ],
        )

        scheduler: BackgroundScheduler = APP_CONTAINER.services.background_scheduler()
        scheduler.add_job(
            APP_CONTAINER.services.lalafo_service().parse,
            IntervalTrigger(minutes=APP_CONTAINER.config.RUN_PARSER_EVERY_MINUTES()),
            max_instances=1,
        )

        scheduler.add_job(
            APP_CONTAINER.services.diesel_service().parse,
            IntervalTrigger(minutes=APP_CONTAINER.config.RUN_PARSER_EVERY_MINUTES()),
            max_instances=1,
        )

        scheduler.start()
