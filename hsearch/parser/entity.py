from dataclasses import dataclass


@dataclass(slots=True)
class ApartmentEntity:
    title: str
    external_id: int
    external_url: str
