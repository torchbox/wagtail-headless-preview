from django.apps import AppConfig


class WagtailHeadlessPreviewTestsAppConfig(AppConfig):
    name = "tests.testapp"
    label = "wagtail_headless_preview_tests"
    verbose_name = "Wagtail Headless Preview tests"
    default_auto_field = "django.db.models.AutoField"
