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

and configure `PREVIEW_URL` to point to your front-end URL.

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
