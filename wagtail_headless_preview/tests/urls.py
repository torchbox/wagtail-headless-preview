from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls

from wagtail_headless_preview.tests.testapp.api import api_router

urlpatterns = [
    url(r"^admin/", include(wagtailadmin_urls)),
    url(r"^api/v2/", api_router.urls),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    url(r"", include(wagtail_urls)),
]
