# [Wagtail Headless Preview](https://pypi.org/project/wagtail-headless-preview/) [![PyPI](https://img.shields.io/pypi/v/wagtail-headless-preview.svg)](https://pypi.org/project/wagtail-headless-preview/)

## Overview

With Wagtail as the backend, and a separate app for the front-end (for example a single page React app), editors are no longer able to preview their changes. This is because the front-end is no longer within Wagtail's direct control. The preview data therefore needs to be exposed to the front-end app.

This package enables previews for Wagtail pages when used in a headless setup by routing the preview to the specified front-end URL.

## Setup

Install using pip:
```sh
pip install wagtail-headless-preview
```

After installing the module, add `wagtail_headless_preview` to installed apps in your settings file:

```python
# settings.py

INSTALLED_APPS = [
    ...
    'wagtail_headless_preview',
]
```

Run migrations:

```sh
$ ./manage.py migrate
```

then configure the preview client URL using the `HEADLESS_PREVIEW_CLIENT_URLS` setting.

For single site, the configuration should look like:

```python
HEADLESS_PREVIEW_CLIENT_URLS = {
    'default': 'http://localhost:8020/',
}
```

For a multi-site setup, add each site as a separate entry:

```python
HEADLESS_PREVIEW_CLIENT_URLS = {
    'default': 'http://localhost:8020/',
    'site1.example.com': 'http://localhost:8020/',
    'site2.example.com': 'http://localhost:8021/',
}
```

Optionally, you can enable live preview functionality with the `HEADLESS_PREVIEW_LIVE` setting:

```python
# settings.py
HEADLESS_PREVIEW_LIVE = True
```

Note: Your front-end app must be set up for live preview, a feature that usually requires [Django Channels](https://github.com/django/channels/) or other WebSocket/async libraries. 

## Usage

Add `HeadlessPreviewMixin` to your page class:

```python
from wagtail_headless_preview.models import HeadlessPreviewMixin

class MyWonderfulPage(HeadlessPreviewMixin, Page):
    pass
```

## How will my front-end app display preview content?

This depends on your project, as it will be dictated by the requirements of your front-end app.

The following example uses a Wagtail API endpoint to access previews - 
your app may opt to access page previews using [GraphQL](https://wagtail.io/blog/getting-started-with-wagtail-and-graphql/) instead.

### Example

This example sets up an API endpoint which will return the preview for a page, and then displays that data on a simplified demo front-end app.

* Add `wagtail.api.v2` to the installed apps:
```python
# settings.py

INSTALLED_APPS = [
    ...
    'wagtail.api.v2',
]
```

* create an `api.py` file in your project directory:
```python
from django.contrib.contenttypes.models import ContentType

from wagtail.api.v2.endpoints import PagesAPIEndpoint
from wagtail.api.v2.router import WagtailAPIRouter

from wagtail_headless_preview.models import PagePreview
from rest_framework.response import Response


# Create the router. "wagtailapi" is the URL namespace
api_router = WagtailAPIRouter('wagtailapi')


class PagePreviewAPIEndpoint(PagesAPIEndpoint):
    known_query_parameters = PagesAPIEndpoint.known_query_parameters.union(['content_type', 'token'])

    def listing_view(self, request):
        page = self.get_object()
        serializer = self.get_serializer(page)
        return Response(serializer.data)

    def detail_view(self, request, pk):
        page = self.get_object()
        serializer = self.get_serializer(page)
        return Response(serializer.data)

    def get_object(self):
        app_label, model = self.request.GET['content_type'].split('.')
        content_type = ContentType.objects.get(app_label=app_label, model=model)

        page_preview = PagePreview.objects.get(content_type=content_type, token=self.request.GET['token'])
        page = page_preview.as_page()
        if not page.pk:
            # fake primary key to stop API URL routing from complaining
            page.pk = 0

        return page


api_router.register_endpoint('page_preview', PagePreviewAPIEndpoint)
```

* Register the API URLs so Django can route requests into the API:

```python
# urls.py

from .api import api_router

urlpatterns = [
    ...
    path('api/v2/', api_router.urls),
    ...
    # Ensure that the api_router line appears above the default Wagtail page serving route
    path('', include(wagtail_urls)),
]
```

For further information about configuring the wagtail API, refer to the [Wagtail API v2 Configuration Guide](https://docs.wagtail.io/en/stable/advanced_topics/api/v2/configuration.html)

* Next, add a `client/index.html` file in your project root. This will query the API to display our preview:

```html
<!DOCTYPE html>
<html>
<head>
    <script>
        function go() {
            var querystring = window.location.search.replace(/^\?/, '');
            var params = {};
            querystring.replace(/([^=&]+)=([^&]*)/g, function(m, key, value) {
                params[decodeURIComponent(key)] = decodeURIComponent(value);
            });

            var apiUrl = 'http://localhost:8000/api/v2/page_preview/1/?content_type=' + encodeURIComponent(params['content_type']) + '&token=' + encodeURIComponent(params['token']) + '&format=json';
            fetch(apiUrl).then(function(response) {
                response.text().then(function(text) {
                    document.body.innerText = text;
                });
            });
        }
    </script>
</head>
<body onload="go()"></body>
</html>
```


* Install django-cors-headers: `pip install django-cors-headers`
* Add CORS config to your settings file to allow the front-end to access the API

```python
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/v2/'
 ```
 
and follow the rest of the [setup instructions for django-cors-headers](https://github.com/ottoyiu/django-cors-headers#setup).

* Start up your site as normal: `./manage.py runserver 0:8000`
* Serve the front-end `client/index.html` at `http://localhost:8020/`
   - this can be done by running `python3 -m http.server 8020` from inside the client directory
* From the wagtail admin interface, edit (or create) and preview a page that uses `HeadlessPreviewMixin`

The preview page should now show you the API response for the preview! 🎉

This is where a real front-end would take over and display the preview as it would be seen on the live site.

## Credits

- Matthew Westcott ([@gasman](https://github.com/gasman)), initial proof of concept
- Karl Hobley ([@kaedroho](https://github.com/kaedroho)), improvements
