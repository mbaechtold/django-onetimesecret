from django.urls import path

from onetimesecret.views import CreateSecret
from onetimesecret.views import ShowSharingInstructions
from onetimesecret.views import ViewSecret

urlpatterns = [
    path("", CreateSecret.as_view(), name="home"),
    path(
        "private/<str:key>/<uuid:uuid>/",
        ShowSharingInstructions.as_view(),
        name="sharing-instructions",
    ),
    path("secret/<str:key>/<uuid:uuid>/", ViewSecret.as_view(), name="view-secret"),
]
