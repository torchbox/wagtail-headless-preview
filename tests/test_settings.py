from unittest.mock import patch

from django.test import TestCase, override_settings
from wagtail_headless_preview.deprecation import pending_deprecation_warning
from wagtail_headless_preview.settings import (
    DEFAULTS,
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

    @patch(
        "wagtail_headless_preview.settings.DEPRECATED_SETTINGS",
        [
            (
                "A_DEPRECATED_SETTING",
                "ENFORCE_TRAILING_SLASH",
                pending_deprecation_warning,
            )
        ],
    )
    def test_warning_raised_on_deprecated_setting(self):
        """
        Make sure user is alerted when a deprecated setting is used.
        """
        msg = (
            "The 'A_DEPRECATED_SETTING' setting is "
            "deprecated and will be removed in the next release, "
            'use WAGTAIL_HEADLESS_PREVIEW["ENFORCE_TRAILING_SLASH"] instead.'
        )
        with self.assertWarnsMessage(PendingDeprecationWarning, msg):
            WagtailHeadlessPreviewSettings({"A_DEPRECATED_SETTING": {}})

        with override_settings(A_DEPRECATED_SETTING="foo"):
            headless_preview_settings = WagtailHeadlessPreviewSettings(None, DEFAULTS)
            with self.assertWarnsMessage(PendingDeprecationWarning, msg):
                self.assertEqual(
                    headless_preview_settings.ENFORCE_TRAILING_SLASH, "foo"
                )

    def test_runtime_error_raised_on_removed_setting(self):
        msg = (
            "The 'HEADLESS_PREVIEW_CLIENT_URLS' setting has been removed. "
            "Please refer to the wagtail_headless_preview documentation for "
            "available settings."
        )
        with self.assertRaisesMessage(RuntimeError, msg):
            WagtailHeadlessPreviewSettings(
                {"HEADLESS_PREVIEW_CLIENT_URLS": "something"}, DEFAULTS
            )

        with patch(
            "wagtail_headless_preview.settings.REMOVED_SETTINGS", ["A_REMOVED_SETTING"]
        ):
            msg = (
                "The 'A_REMOVED_SETTING' setting has been removed. "
                "Please refer to the wagtail_headless_preview documentation "
                "for available settings."
            )
            with self.assertRaisesMessage(RuntimeError, msg):
                WagtailHeadlessPreviewSettings({"A_REMOVED_SETTING": "something"})
