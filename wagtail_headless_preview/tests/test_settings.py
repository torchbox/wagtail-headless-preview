from unittest.mock import patch

from django.test import TestCase, override_settings

from wagtail_headless_preview.settings import (
    WagtailHeadlessPreviewSettings,
    headless_preview_settings,
)


class SettingsTests(TestCase):
    def test_compatibility_with_override_settings(self):
        default_client_urls = {
            "default": "http://localhost:8020/"
        }  # set in test app settings
        self.assertDictEqual(
            headless_preview_settings.CLIENT_URLS,
            default_client_urls,
            "Checking a known default",
        )

        with override_settings(
            WAGTAIL_HEADLESS_PREVIEW={
                "CLIENT_URLS": {"default": "https://headless.site"}
            }
        ):
            self.assertDictEqual(
                headless_preview_settings.CLIENT_URLS,
                {"default": "https://headless.site"},
                "Setting should have been updated",
            )

        self.assertDictEqual(
            headless_preview_settings.CLIENT_URLS,
            default_client_urls,
            "Setting should have been restored",
        )

    def test_warning_raised_on_deprecated_setting(self):
        """
        Make sure user is alerted with an deprecated setting is used.
        """
        msg = (
            "The 'HEADLESS_PREVIEW_CLIENT_URLS' setting is "
            "deprecated and will be removed in the next release, "
            'use WAGTAIL_HEADLESS_PREVIEW["CLIENT_URLS"] instead.'
        )
        with self.assertWarnsMessage(PendingDeprecationWarning, msg):
            WagtailHeadlessPreviewSettings({"HEADLESS_PREVIEW_CLIENT_URLS": {}})

    @patch("wagtail_headless_preview.settings.REMOVED_SETTINGS", ["A_REMOVED_SETTING"])
    def test_runtime_error_raised_on_removed_setting(self):
        msg = (
            "The 'A_REMOVED_SETTING' setting has been removed. "
            "Please refer to the wagtail_headless_preview documentation for available settings."
        )
        with self.assertRaisesMessage(RuntimeError, msg):
            WagtailHeadlessPreviewSettings({"A_REMOVED_SETTING": "something"})
