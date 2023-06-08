import datetime
import json

from django.contrib.contenttypes.models import ContentType
from django.core.signing import TimestampSigner
from django.db import models
from django.shortcuts import redirect, render
from django.utils.http import urlencode

from wagtail_headless_preview.settings import headless_preview_settings
from wagtail_headless_preview.signals import preview_update


class PagePreview(models.Model):
    token = models.CharField(max_length=255, unique=True)
    content_type = models.ForeignKey(
        "contenttypes.ContentType", on_delete=models.CASCADE
    )
    content_json = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def as_page(self):
        content = json.loads(self.content_json)
        page_model = ContentType.objects.get_for_id(
            content["content_type"]
        ).model_class()
        page = page_model.from_json(self.content_json)
        page.pk = content["pk"]
        return page

    @classmethod
    def garbage_collect(cls):
        yesterday = datetime.datetime.now() - datetime.timedelta(hours=24)
        cls.objects.filter(created_at__lt=yesterday).delete()


def get_client_root_url_from_site(site):
    try:
        root_url = headless_preview_settings.CLIENT_URLS[site.hostname]
    except (AttributeError, KeyError):
        root_url = headless_preview_settings.CLIENT_URLS["default"].format(
            SITE_ROOT_URL=site.root_url
        )

    if headless_preview_settings.ENFORCE_TRAILING_SLASH:
        root_url = root_url.rstrip("/") + "/"

    return root_url


class HeadlessPreviewMixin:
    @classmethod
    def get_preview_signer(cls):
        return TimestampSigner(salt="headlesspreview.token")

    @classmethod
    def get_content_type_str(cls):
        return cls._meta.app_label + "." + cls.__name__.lower()

    @classmethod
    def get_page_from_preview_token(cls, token):
        content_type = ContentType.objects.get_for_model(cls)

        # Check token is valid
        cls.get_preview_signer().unsign(token)

        try:
            return PagePreview.objects.get(
                content_type=content_type, token=token
            ).as_page()
        except PagePreview.DoesNotExist:
            return

    def create_page_preview(self):
        if self.pk is None:
            identifier = (
                f"parent_id={self.get_parent().pk};page_type={self._meta.label}"
            )
        else:
            identifier = f"id={self.pk}"

        token = self.get_preview_signer().sign(identifier)
        # Note: Using update_page_preview() instead of just create() to avoid
        # unique constraint failures if preview is clicked multiple times
        preview, _ = self.update_page_preview(token)

        return preview

    def update_page_preview(self, token):
        return PagePreview.objects.update_or_create(
            token=token,
            defaults={
                "content_type": self.content_type,
                "content_json": self.to_json(),
            },
        )

    def get_client_root_url(self):
        return get_client_root_url_from_site(self.get_site())

    def get_preview_url(self, token):
        return (
            self.get_client_root_url()
            + "?"
            + urlencode({"content_type": self.get_content_type_str(), "token": token})
        )

    def serve_preview(self, request, preview_mode):
        PagePreview.garbage_collect()
        page_preview = self.create_page_preview()
        page_preview.save()

        # Send the preview_update signal. Other apps can implement their own handling
        preview_update.send(sender=HeadlessPreviewMixin, token=page_preview.token)

        preview_url = self.get_preview_url(page_preview.token)
        if headless_preview_settings.REDIRECT_ON_PREVIEW:
            return redirect(preview_url)

        response = render(
            request,
            "wagtail_headless_preview/preview.html",
            {"preview_url": preview_url},
        )

        return response


class HeadlessServeMixin:
    def serve(self, request):
        """
        Mixin overriding the default serve method with a redirect.
        The URL of the requested page is kept the same, only the host is
        overridden.
        By default, this uses the hosts defined in HEADLESS_PREVIEW_CLIENT_URLS.
        However, you can enforce a single host using the HEADLESS_SERVE_BASE_URL
        setting.
        """
        if headless_preview_settings.SERVE_BASE_URL:
            base_url = headless_preview_settings.SERVE_BASE_URL
        else:
            base_url = get_client_root_url_from_site(self.get_site())
        site_id, site_root, relative_page_url = self.get_url_parts(request)
        return redirect(f"{base_url.rstrip('/')}{relative_page_url}")


class HeadlessMixin(HeadlessPreviewMixin, HeadlessServeMixin):
    pass
