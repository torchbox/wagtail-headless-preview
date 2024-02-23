from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse
from django.utils.http import urlencode
from wagtail.models import Page

from tests.testapp.models import HeadlessPage, SimplePage
from wagtail_headless_preview.models import PagePreview
from wagtail_headless_preview.settings import headless_preview_settings


class TestMixins(TestCase):
    fixtures = ["test.json"]

    @classmethod
    def setUpTestData(cls):
        cls.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",
        )

        cls.homepage = Page.objects.get(url_path="/home/").specific
        cls.page = SimplePage(title="Simple page original", slug="simple-page")
        cls.homepage.add_child(instance=cls.page)

        cls.page.title = "Simple page submitted"
        cls.page.save_revision()

        cls.page.title = "Simple page with draft edit"
        cls.page.save_revision()

        cls.headless_page = HeadlessPage(
            title="Headless page original", slug="headless-page"
        )
        cls.homepage.add_child(instance=cls.headless_page)

        cls.request = RequestFactory().get("/")

    def setUp(self):
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
        self.assertContains(
            response,
            urlencode({"content_type": "wagtail_headless_preview_tests.simplepage"}),
        )

        params = {
            "content_type": "wagtail_headless_preview_tests.simplepage",
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

    @override_settings(
        WAGTAIL_HEADLESS_PREVIEW={
            "CLIENT_URLS": {"default": "https://headless.site"},
            "REDIRECT_ON_PREVIEW": True,
        }
    )
    def test_redirect_on_preview(self):
        view_draft_url = reverse("wagtailadmin_pages:view_draft", args=(self.page.id,))
        response = self.client.get(view_draft_url)

        preview_token = PagePreview.objects.first().token

        self.assertRedirects(
            response,
            self.page.get_preview_url(self.request, preview_token),
            fetch_redirect_response=False,
        )

    @override_settings(
        WAGTAIL_HEADLESS_PREVIEW={"CLIENT_URLS": {"default": "https://headless.site"}}
    )
    def test_get_client_root_url_with_default_trailing_slash_enforcement(self):
        self.assertEqual(
            self.page.get_client_root_url(self.request),
            "https://headless.site/",
        )

    @override_settings(
        WAGTAIL_HEADLESS_PREVIEW={
            "CLIENT_URLS": {"default": "https://headless.site"},
            "ENFORCE_TRAILING_SLASH": False,
        }
    )
    def test_get_client_root_url_without_trailing_slash_enforcement(self):
        self.assertEqual(
            self.page.get_client_root_url(self.request),
            "https://headless.site",
        )

    @override_settings(
        WAGTAIL_HEADLESS_PREVIEW={"SERVE_BASE_URL": "https://headless.site"},
        TEST_OVERRIDE_CLIENT_ROOT_URL=True,
    )
    def test_get_client_root_url_override_in_implementing_page(self):
        self.assertEqual(
            self.headless_page.get_client_root_url(self.request),
            "https://wagtail.org",
        )

    def test_create_page_preview_race(self):
        self.page.create_page_preview()

        self.page.title = "Another edit so JSON changes"
        self.page.save_revision()

        # This shouldn't hit a unique constraint error
        self.page.create_page_preview()

    def test_headless_serve_mixin_redirects_in_serve(self):
        client_url = headless_preview_settings.CLIENT_URLS["default"].rstrip("/")
        response = self.client.get(self.headless_page.url)
        self.assertRedirects(
            response,
            f"{client_url}/{self.headless_page.slug}/",
            fetch_redirect_response=False,
        )

    @override_settings(
        WAGTAIL_HEADLESS_PREVIEW={"SERVE_BASE_URL": "https://headless.site"}
    )
    def test_headless_serve_mixin_serve_with_headless_serve_base_url(self):
        response = self.client.get(self.headless_page.url)
        self.assertRedirects(
            response,
            f"https://headless.site/{self.headless_page.slug}/",
            fetch_redirect_response=False,
        )
