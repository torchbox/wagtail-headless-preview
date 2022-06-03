from django.conf import settings
from django.utils.html import format_html_join


try:
    from wagtail import hooks
except ImportError:
    # Wagtail<3.0
    from wagtail.core import hooks

from wagtail_headless_preview.settings import headless_preview_settings


@hooks.register("insert_editor_js")
def editor_js():
    if not headless_preview_settings.LIVE_PREVIEW:
        return ""

    js_files = ["js/live-preview.js"]

    return format_html_join(
        "\n",
        '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files),
    )
