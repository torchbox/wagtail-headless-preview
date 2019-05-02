# Wagtail Headless Preview

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


## Usage

Add `HeadlessPreviewMixin` to your page class:

```python
from wagtail_headless_preview.models import HeadlessPreviewMixin

class MyWonderfulPage(HeadlessPreviewMixin, Page):
    pass
```

## How do I access preview content?

It depends on your project.

For a quick test: 

* Add `wagtail.api.v2` to the installed apps:
```python
# settings.py

INSTALLED_APPS = [
    ...
    'wagtail.api.v2',
]
```

* Register the the API URLs so Django can route requests into the API:

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

For further details, refer to the [Wagtail API v2 Configuration Guide](https://docs.wagtail.io/en/stable/advanced_topics/api/v2/configuration.html)

* Next, add a `client/index.html` file in your project root:

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
* Add to your settings file 
```python
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/v2/'
 ``` 

* Start up your site as normal: `./manage.py runserver 0:8000`
* Set up `client/index.html` to be served at `http://localhost:8020/` - 
  this can be done by running `python3 -m http.server 8020` from inside the client directory
* Edit (or created) and preview a page that uses `HeadlessPreviewMixin`
* The preview page should now show you the API response for the preview

## Credits

- Matthew Westcott ([@gasman](https://github.com/gasman)), initial proof of concept
- Karl Hobley ([@kaedroho](https://github.com/kaedroho)), improvements
