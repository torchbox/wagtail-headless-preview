from wagtail.core.models import Page

from wagtail_headless_preview.models import HeadlessPreviewMixin


class SimplePage(HeadlessPreviewMixin, Page):
    pass
