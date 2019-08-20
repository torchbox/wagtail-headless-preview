from django.contrib.contenttypes.models import ContentType

from rest_framework.response import Response
from wagtail.api.v2.endpoints import PagesAPIEndpoint
from wagtail.api.v2.router import WagtailAPIRouter

from wagtail_headless_preview.models import PagePreview

# Create the router. "wagtailapi" is the URL namespace
api_router = WagtailAPIRouter("wagtailapi_v2")


class PagePreviewAPIEndpoint(PagesAPIEndpoint):
    known_query_parameters = PagesAPIEndpoint.known_query_parameters.union(
        ["content_type", "token"]
    )

    def listing_view(self, request):
        page = self.get_object()
        serializer = self.get_serializer(page)
        return Response(serializer.data)

    def detail_view(self, request, pk):
        page = self.get_object()
        serializer = self.get_serializer(page)
        return Response(serializer.data)

    def get_object(self):
        app_label, model = self.request.GET["content_type"].split(".")
        content_type = ContentType.objects.get(app_label=app_label, model=model)

        page_preview = PagePreview.objects.get(
            content_type=content_type, token=self.request.GET["token"]
        )
        page = page_preview.as_page()
        if not page.pk:
            # fake primary key to stop API URL routing from complaining
            page.pk = 0

        return page


api_router.register_endpoint("page_preview", PagePreviewAPIEndpoint)
