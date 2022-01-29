from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.http import urlencode

from wagtail.core.models import Page

from wagtail_headless_preview.models import PagePreview
from wagtail_headless_preview.tests.testapp.models import HeadlessPage, SimplePage


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

        self.client.login(username=self.admin_user.username, password="password")

    def test_view(self):
        self.assertEqual(PagePreview.objects.count(), 0)
        # Try getting page draft
        view_draft_url = reverse("wagtailadmin_pages:view_draft", args=(self.page.id,))
        response = self.client.get(view_draft_url)

        # User can view
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PagePreview.objects.count(), 1)

        preview_token = PagePreview.objects.first().token
        self.assertContains(response, urlencode({"token": preview_token}))
        self.assertContains(response, urlencode({"content_type": "testapp.simplepage"}))

        params = {
            "content_type": "testapp.simplepage",
            "token": preview_token,
            "format": "json",
        }
        preview_url = "{base_url}{page_id}/?{params}".format(
            base_url=reverse("wagtailapi_v2:page_preview:listing"),
            page_id=self.page.id,
            params=urlencode(params),
        )
        response = self.client.get(preview_url)
        self.assertContains(response, "Simple page with draft edit")

    @override_settings(HEADLESS_PREVIEW_REDIRECT=True)
    def test_redirect_on_preview(self):
        view_draft_url = reverse("wagtailadmin_pages:view_draft", args=(self.page.id,))
        response = self.client.get(view_draft_url)

        preview_token = PagePreview.objects.first().token

        self.assertRedirects(
            response,
            self.page.get_preview_url(preview_token),
            fetch_redirect_response=False,
        )


class TestHeadlessRedirectMixin(TestCase):
    fixtures = ["test.json"]

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )

        self.homepage = Page.objects.get(url_path="/home/").specific
        self.page = HeadlessPage(title="Simple page original", slug="simple-page")
        self.homepage.add_child(instance=self.page)

    def test_serve(self):
        client_url = settings.HEADLESS_PREVIEW_CLIENT_URLS["default"].rstrip("/")
        response = self.client.get(self.page.url)
        self.assertRedirects(
            response, f"{client_url}/{self.page.slug}/", fetch_redirect_response=False
        )

    @override_settings(HEADLESS_SERVE_BASE_URL="https://headless.site")
    def test_serve_with_headless_serve_base_url(self):
        response = self.client.get(self.page.url)
        self.assertRedirects(
            response,
            f"https://headless.site/{self.page.slug}/",
            fetch_redirect_response=False,
        )
