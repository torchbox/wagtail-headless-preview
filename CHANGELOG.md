# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Add support for a `{SITE_ROOT_URL}` placeholder in "default" preview client url ([#20](https://github.com/torchbox/wagtail-headless-preview/pull/20)) - Thanks @jaap3
- Add [pre-commit](https://pre-commit.com/) support ([#21](https://github.com/torchbox/wagtail-headless-preview/pull/21)) - @zerolab
- Add `HeadlessMixin` and `HeadlessServeMixin` ([#22](https://github.com/torchbox/wagtail-headless-preview/pull/22)) - @zerolab
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


## [0.1.0] - 2019-08-20

### Added

- Live preview functionality
- Better error handling
- Garbage collect before creating new preview

## [0.0.2] - 2019-05-01

Initial release

[unreleased]: https://github.com/wagtail/wagtail-localize/compare/v1.0.1...HEAD
[0.1.4]: https://github.com/wagtail/wagtail-localize/compare/v0.1.4...v0.1.0
[0.1.0]: https://github.com/wagtail/wagtail-localize/compare/v0.1.0..v0.0.2
