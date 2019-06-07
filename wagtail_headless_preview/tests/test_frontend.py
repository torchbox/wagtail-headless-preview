from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from wagtail.core.models import Page

from wagtail_headless_preview.tests.testapp.models import SimplePage


class TestFrontendViews(TestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='password'
        )

        self.homepage = Page.objects.get(url_path='/home/').specific
        self.page = SimplePage(title="Simple page original", slug="simple-page")
        self.homepage.add_child(instance=self.page)

        self.page.title = "Simple page submitted"
        self.page.save_revision()

        self.page.title = "Simple page with draft edit"
        self.page.save_revision()

    def test_view(self):
        # Try getting page draft
        response = self.client.get(reverse('wagtailadmin_pages:view_draft', args=(self.page.id,)))

        # User can view
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<title>Headless preview</title>')
        self.assertContains(response, 'Simple page with draft edit')
