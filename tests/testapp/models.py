from wagtail.core.models import Page

from wagtail_headless_preview.models import HeadlessMixin, HeadlessPreviewMixin


class SimplePage(HeadlessPreviewMixin, Page):
    pass


class HeadlessPage(HeadlessMixin, Page):
    pass
