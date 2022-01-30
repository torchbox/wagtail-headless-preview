default_app_config = "wagtail_headless_preview.apps.WagtailHeadlessPreviewConfig"

VERSION = (0, 1, 4)
__version__ = ".".join(map(str, VERSION))


def setup():
    import warnings

    from .deprecation import removed_in_next_version_warning

    warnings.simplefilter("default", removed_in_next_version_warning)


setup()
