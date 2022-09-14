"""
The wagtail_headless_preview settings are namespaced in the WAGTAIL_HEADLESS_PREVIEW setting.
For example your project's `settings.py` file might look like this:
WAGTAIL_HEADLESS_PREVIEW = {
    "CLIENT_URLS": {"default": "https://headless.site"},
    # ...
}
This module provides the `headless_preview_settings` object, that is used to access
the settings. It checks for user settings first, with fallback to defaults.
"""
import warnings

from django.conf import settings
from django.test.signals import setting_changed


DEFAULTS = {
    "CLIENT_URLS": {},
    "LIVE_PREVIEW": False,
    "SERVE_BASE_URL": None,
    "REDIRECT_ON_PREVIEW": False,
    "ENFORCE_TRAILING_SLASH": True,
}

# List of settings that have been deprecated
DEPRECATED_SETTINGS = []

# List of settings that have been removed
REMOVED_SETTINGS = ["HEADLESS_PREVIEW_CLIENT_URLS", "HEADLESS_PREVIEW_LIVE"]


class WagtailHeadlessPreviewSettings:
    """
    A settings object that allows the wagtail_headless_preview settings to be accessed as
    properties. For example:
        from wagtail_headless_previews.settings import headless_preview_settings
        print(headless_preview_settings.CLIENT_URLS)
    Note:
    This is an internal class that is only compatible with settings namespaced
    under the WAGTAIL_HEADLESS_PREVIEW name. It is not intended to be used by 3rd-party
    apps, and test helpers like `override_settings` may not work as expected.
    """

    def __init__(self, user_settings=None, defaults=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or DEFAULTS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = self.__check_user_settings(
                getattr(settings, "WAGTAIL_HEADLESS_PREVIEW", {})
            )
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError(
                "Invalid wagtail_headless_preview setting: '%s'" % attr
            )

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        for old_setting, new_setting, category in DEPRECATED_SETTINGS:
            setting_in_user_settings = old_setting in user_settings
            if setting_in_user_settings or hasattr(settings, old_setting):
                warnings.warn(
                    f"The '{old_setting}' setting is deprecated and will be "
                    f"removed in the next release, use "
                    f'WAGTAIL_HEADLESS_PREVIEW["{new_setting}"] instead.',
                    category=category,
                )
                if setting_in_user_settings:
                    user_settings[new_setting] = user_settings[old_setting]
                else:
                    user_settings[new_setting] = getattr(settings, old_setting)

        for removed_setting in REMOVED_SETTINGS:
            if removed_setting in user_settings or hasattr(settings, removed_setting):
                raise RuntimeError(
                    f"The '{removed_setting}' setting has been removed. "
                    f"Please refer to the wagtail_headless_preview "
                    f"documentation for available settings."
                )
        return user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")


headless_preview_settings = WagtailHeadlessPreviewSettings(None, DEFAULTS)


def reload_headless_preview_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == "WAGTAIL_HEADLESS_PREVIEW":
        headless_preview_settings.reload()


setting_changed.connect(reload_headless_preview_settings)
