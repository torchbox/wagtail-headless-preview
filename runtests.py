#!/usr/bin/env python
import argparse
import os
import sys
import warnings

from django.core.management import execute_from_command_line


os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--deprecation",
        choices=["all", "pending", "imminent", "none"],
        default="imminent",
    )
    return parser.parse_known_args(args)


def runtests():
    args, rest = parse_args()

    only_wagtail = r"^wagtail(\.|$)"
    only_wagtail_headless_preview = r"^wagtail_headless_preview(\.|$)"
    if args.deprecation == "all":
        # Show all deprecation warnings from all packages
        warnings.simplefilter("default", DeprecationWarning)
        warnings.simplefilter("default", PendingDeprecationWarning)
    elif args.deprecation == "pending":
        # Show all deprecation warnings from Wagtail
        warnings.filterwarnings(
            "default", category=DeprecationWarning, module=only_wagtail
        )
        warnings.filterwarnings(
            "default", category=PendingDeprecationWarning, module=only_wagtail
        )

        # and all from wagtail_headless_preview
        warnings.filterwarnings(
            "default", category=DeprecationWarning, module=only_wagtail_headless_preview
        )
        warnings.filterwarnings(
            "default",
            category=PendingDeprecationWarning,
            module=only_wagtail_headless_preview,
        )
    elif args.deprecation == "imminent":
        # Show only imminent deprecation warnings
        warnings.filterwarnings(
            "default", category=DeprecationWarning, module=only_wagtail
        )
        warnings.filterwarnings(
            "default", category=DeprecationWarning, module=only_wagtail_headless_preview
        )
    elif args.deprecation == "none":
        # Deprecation warnings are ignored by default
        pass

    argv = [sys.argv[0]] + rest

    try:
        execute_from_command_line(argv)
    finally:
        pass


if __name__ == "__main__":
    runtests()
