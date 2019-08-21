from django.conf import settings
from django.utils.html import format_html_join

from wagtail.core import hooks


@hooks.register("insert_editor_js")
def editor_js():
    if hasattr(settings, "HEADLESS_PREVIEW_LIVE") and settings.HEADLESS_PREVIEW_LIVE:
        js_files = ["js/live-preview.js"]

        return format_html_join(
            "\n",
            '<script src="{0}{1}"></script>',
            ((settings.STATIC_URL, filename) for filename in js_files),
        )

    return ""
