#!/usr/bin/env python

import os
import sys
import warnings

from django.core.management import execute_from_command_line


os.environ["DJANGO_SETTINGS_MODULE"] = "wagtail_headless_preview.tests.settings"


def runtests():
    # Don't ignore DeprecationWarnings
    only_wagtail_headless_preview = r"^wagtail_headless_preview(\.|$)"
    warnings.filterwarnings(
        "default", category=DeprecationWarning, module=only_wagtail_headless_preview
    )
    warnings.filterwarnings(
        "default",
        category=PendingDeprecationWarning,
        module=only_wagtail_headless_preview,
    )

    args = sys.argv[1:]
    argv = sys.argv[:1] + ["test"] + args
    try:
        execute_from_command_line(argv)
    finally:
        pass


if __name__ == "__main__":
    runtests()
