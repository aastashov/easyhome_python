"""Containers module."""
from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler
from dependency_injector import containers, providers

from easyhome.parser.http_client import HttpClient
from easyhome.parser.services import ParseSiteService
from easyhome.parser.sites.diesel import Diesel
from easyhome.parser.sites.house import House
from easyhome.parser.sites.lalafo import Lalafo


class ServicesContainer(containers.DeclarativeContainer):
    """Container containing all project's services."""

    config = providers.Configuration()

    background_scheduler: providers.Provider[BackgroundScheduler] = providers.Singleton(BackgroundScheduler)

    lalafo_site = providers.Factory(Lalafo)
    diesel_site = providers.Factory(Diesel)
    house_site = providers.Factory(House)

    http_client = providers.Singleton(HttpClient)

    lalafo_service = providers.Factory(
        ParseSiteService,
        http_client=http_client,
        site=lalafo_site,
    )

    diesel_service = providers.Factory(
        ParseSiteService,
        http_client=http_client,
        site=diesel_site,
    )

    house_service = providers.Factory(
        ParseSiteService,
        http_client=http_client,
        site=house_site,
    )
