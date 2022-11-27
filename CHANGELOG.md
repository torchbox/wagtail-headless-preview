# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5] - 2022-11-27

### Fixed

- Race condition in `create_page_view` ([#35](https://github.com/torchbox/wagtail-headless-preview/pull/35)) @johncarter-phntm

### Removed

- `LIVE_PREVIEW` setting and related code. It was not fit for purpose

## [0.4] - 2022-09-14

### Added

- New `ENFORCE_TRAILING_SLASH` setting option to control the trailing slash on the preview URLs.
- Official support for Wagtail 4.0, plus PyPI trove classifiers

### Removed

- Removed support for the deprecated `HEADLESS_PREVIEW_CLIENT_URLS` and `HEADLESS_PREVIEW_LIVE`. You should
  see a runtime error if you are still using these settings.

## [0.3] - 2022-06-05

### Added

 - Support for Wagtail 3.0

### Removed
 - Removed support for Wagtail < 2.15, Django < 3.2

## [0.2.1] - 2022-02-01

## Fixed
- Deprecated settings not handled correctly. Thanks to @Schille for the report.

## [0.2] - 2022-01-30

This release adds a number of useful features such as a default client URL placeholder,
ability to redirect to the front-end URLs when viewing a page in the Wagtail admin, and
an option to redirect the preview to the client URL rather than use the default iframe embed mechanism.

It also moves to a single, namespaced settings dictionary - `WAGTAIL_HEADLESS_PREVIEW`:

```python
WAGTAIL_HEADLESS_PREVIEW = {
    "CLIENT_URLS": {},  # previously HEADLESS_PREVIEW_CLIENTS_URLS
    "LIVE_PREVIEW": False,  # previously HEADLESS_PREVIEW_LIVE
    "SERVE_BASE_URL": None,  # new optional setting for HeadlessServeMixin / HeadlessMixin
    "REDIRECT_ON_PREVIEW": False,  # new optional setting to redirect the preview to the client preview URL
}
```

### Added

- Add support for a `{SITE_ROOT_URL}` placeholder in "default" preview client URL ([#20](https://github.com/torchbox/wagtail-headless-preview/pull/20)) - Thanks @jaap3
- Add [pre-commit](https://pre-commit.com/) support ([#21](https://github.com/torchbox/wagtail-headless-preview/pull/21)) - @zerolab
- Add `HeadlessMixin` and `HeadlessServeMixin` ([#22](https://github.com/torchbox/wagtail-headless-preview/pull/22)) - @zerolab based on code from @tbrlpld
- Add setting to redirect to the client preview URL ([#23](https://github.com/torchbox/wagtail-headless-preview/pull/23)) - @zerolab based on real world code from @jaap3

### Changed

- Move to GitHub Actions ([#21](https://github.com/torchbox/wagtail-headless-preview/pull/21))
- Update test targets, including Python 3.10 and Django 4.0 ([#21](https://github.com/torchbox/wagtail-headless-preview/pull/21))
- Move to a single, namespaced settings dictionary ([#24](https://github.com/torchbox/wagtail-headless-preview/pull/24)) - @zerolab
- Updated repository structure for lighter packages ([#25](https://github.com/torchbox/wagtail-headless-preview/pull/25))


## [0.1.4] - 2019-08-21

### Added
- Linting with [black](https://github.com/psf/black)

### Fixed
- `UNIQUE constraint failed: wagtail_headless_preview_pagepreview.token`
- Static files not packaged
- Wrong JS file loaded for live preview
- Wrong token used in live preview.
- Explicit utf-8 encoding for long description to fix `UnicodeDecodeError: 'ascii' codec can't decode byte 0xf0 in position 6282: ordinal not in range(128)`
  on some systems when trying to `pip install`


## [0.1] - 2019-08-20

### Added

- Live preview functionality
- Better error handling
- Garbage collect before creating new preview

## [0.0.2] - 2019-05-01

Initial release

[unreleased]: https://github.com/torchbox/wagtail-headless-preview/compare/v0.4.0...HEAD
[0.4]: https://github.com/torchbox/wagtail-headless-preview/compare/v0.3.0...v0.4.0
[0.3]: https://github.com/torchbox/wagtail-headless-preview/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/torchbox/wagtail-headless-preview/compare/v0.2.0...v0.2.1
[0.2]: https://github.com/torchbox/wagtail-headless-preview/compare/v0.1.4...v0.2.0
[0.1.4]: https://github.com/torchbox/wagtail-headless-preview/compare/v0.1.0...v0.1.4
[0.1]: https://github.com/torchbox/wagtail-headless-preview/compare/c84cb15...v0.1.0
