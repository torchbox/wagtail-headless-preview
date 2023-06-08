from django.conf.urls import include
from django.urls import path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls

from tests.testapp.api import api_router


urlpatterns = [
    path("admin/", include(wagtailadmin_urls)),
    path("api/v2/", api_router.urls),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    path("", include(wagtail_urls)),
]
