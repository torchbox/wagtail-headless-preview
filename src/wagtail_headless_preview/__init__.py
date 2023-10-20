VERSION = (0, 7, 0)
__version__ = ".".join(map(str, VERSION))


def setup():
    import warnings

    from .deprecation import removed_in_next_version_warning

    warnings.simplefilter("default", removed_in_next_version_warning)


setup()
