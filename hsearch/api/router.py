from django.contrib.admin.views.decorators import staff_member_required
from ninja import NinjaAPI

from hsearch.api.v1.handlers import apartment, profile

api_v1 = NinjaAPI(
    version="1.0.0",
    title="House Search API",
    docs_decorator=staff_member_required,
)

api_v1.add_router("/apartment", apartment.router)
api_v1.add_router("/profile", profile.router)
