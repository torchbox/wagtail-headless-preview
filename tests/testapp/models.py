from typing import TYPE_CHECKING

from django.conf import settings
from wagtail.models import Page

from wagtail_headless_preview.models import HeadlessMixin, HeadlessPreviewMixin


if TYPE_CHECKING:
    from django.http import HttpRequest


class SimplePage(HeadlessPreviewMixin, Page):
    pass


class HeadlessPage(HeadlessMixin, Page):
    def get_client_root_url(self, request: "HttpRequest") -> str:
        if getattr(settings, "TEST_OVERRIDE_CLIENT_ROOT_URL", False):
            return "https://wagtail.org"

        return super().get_client_root_url(request)
