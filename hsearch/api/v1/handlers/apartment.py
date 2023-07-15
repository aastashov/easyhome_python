from django.http import HttpRequest
from ninja import Router

from hsearch.api.v1 import schemas
from hsearch.hsearch.models import Apartment

router = Router(tags=["Apartment"])


@router.get(
    "/list",
    response=list[schemas.ApartmentResponse],
    summary="Returns a list of all apartments.",
)
def list_appartment_view(request: HttpRequest) -> list[schemas.ApartmentResponse]:
    return Apartment.objects.all()
