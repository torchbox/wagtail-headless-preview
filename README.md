# Wagtail Headless Preview

## Setup

Install using pip:
```sh
pip install wagtail-headless-preview
```

After installing the module, add `wagtail_headless_preview` to installed apps in your settings file:

```python
INSTALLED_APPS = [
    ...
    'wagtail_headless_preview',
]
```

then configure the preview client URL.

For a multi-site setup, you can use `HEADLESS_PREVIEW_CLIENT_URLS`:

```python
HEADLESS_PREVIEW_CLIENT_URLS = {
    'default': 'http://localhost:8020/',
    'site1.example.com': 'http://localhost:8020/',
    'site2.example.com': 'http://localhost:8021/',
}
```

For single sites, the configuration can be:

```python
HEADLESS_PREVIEW_CLIENT_URLS = {
    'default': 'http://localhost:8020/',
}
```

Alternatively, you can use `HEADLESS_PREVIEW_CLIENT_URL`:

```python
HEADLESS_PREVIEW_CLIENT_URL = 'http://localhost:8020/'
```

## Usage

Add `HeadlessPreviewMixin` to your page class:

```python
from wagtail_headless_preview.models import HeadlessPreviewMixin

class MyWonderfulPage(HeadlessPreviewMixin, Page):
    pass
```

## Credits

- Matthew Westcott ([@gasman](https://github.com/gasman)), initial proof of concept
- Karl Hobley ([@kaedroho](https://github.com/kaedroho)), improvements
