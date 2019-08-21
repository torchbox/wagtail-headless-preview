import urllib

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from wagtail.core.models import Page

from wagtail_headless_preview.models import PagePreview
from wagtail_headless_preview.tests.testapp.models import SimplePage


class TestFrontendViews(TestCase):
    fixtures = ["test.json"]

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )

        self.homepage = Page.objects.get(url_path="/home/").specific
        self.page = SimplePage(title="Simple page original", slug="simple-page")
        self.homepage.add_child(instance=self.page)

        self.page.title = "Simple page submitted"
        self.page.save_revision()

        self.page.title = "Simple page with draft edit"
        self.page.save_revision()

    def test_view(self):
        self.client.login(username=self.admin_user.username, password="password")

        self.assertEqual(PagePreview.objects.count(), 0)
        # Try getting page draft
        view_draft_url = reverse("wagtailadmin_pages:view_draft", args=(self.page.id,))
        response = self.client.get(view_draft_url)

        # User can view
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PagePreview.objects.count(), 1)

        preview_token = PagePreview.objects.first().token
        self.assertContains(response, urllib.parse.urlencode({"token": preview_token}))
        self.assertContains(
            response, urllib.parse.urlencode({"content_type": "testapp.simplepage"})
        )

        params = {
            "content_type": "testapp.simplepage",
            "token": preview_token,
            "format": "json",
        }
        preview_api_url = "{base_url}{page_id}/?{params}".format(
            base_url=reverse("wagtailapi_v2:page_preview:listing"),
            page_id=self.page.id,
            params=urllib.parse.urlencode(params),
        )

        response = self.client.get(preview_api_url)
        self.assertContains(response, "Simple page with draft edit")

        # TODO fix this.
        # response = self.client.get(self.page.get_preview_url(preview_token))
        # self.assertContains(response, '<title>Headless preview</title>')
