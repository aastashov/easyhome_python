"""Containers module."""
from __future__ import annotations

from dependency_injector import containers, providers

from .services import ServicesContainer


class ApplicationContainer(containers.DeclarativeContainer):
    """Main container describing all project dependencies."""

    config = providers.Configuration()

    services = providers.Container(ServicesContainer, config=config)
