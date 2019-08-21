import datetime
import json
import urllib

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.signing import TimestampSigner
from django.db import models
from django.shortcuts import render


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


class HeadlessPreviewMixin:
    @classmethod
    def get_preview_signer(cls):
        return TimestampSigner(salt="headlesspreview.token")

    def create_page_preview(self):
        if self.pk is None:
            identifier = "parent_id=%d;page_type=%s" % (
                self.get_parent().pk,
                self._meta.label,
            )
        else:
            identifier = "id=%d" % self.pk

        # Note: Using get_or_create() instead of just create() to avoid unique constraint failures if
        # preview is clicked multiple times
        preview, _ = PagePreview.objects.get_or_create(
            token=self.get_preview_signer().sign(identifier),
            content_type=self.content_type,
            content_json=self.to_json(),
        )
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
        try:
            return settings.HEADLESS_PREVIEW_CLIENT_URLS[self.get_site().hostname]
        except (AttributeError, KeyError):
            return settings.HEADLESS_PREVIEW_CLIENT_URLS["default"]

    @classmethod
    def get_content_type_str(cls):
        return cls._meta.app_label + "." + cls.__name__.lower()

    def get_preview_url(self, token):
        return (
            self.get_client_root_url()
            + "?"
            + urllib.parse.urlencode(
                {"content_type": self.get_content_type_str(), "token": token}
            )
        )

    def dummy_request(self, original_request=None, **meta):
        request = super(HeadlessPreviewMixin, self).dummy_request(
            original_request=original_request, **meta
        )
        request.GET = request.GET.copy()
        request.GET["live_preview"] = original_request.GET.get("live_preview")
        return request

    def serve_preview(self, request, mode_name):
        use_live_preview = request.GET.get("live_preview")
        token = request.COOKIES.get("used-token")

        if use_live_preview and token:
            page_preview, existed = self.update_page_preview(token)
            PagePreview.garbage_collect()

            from wagtail_headless_preview.signals import (
                preview_update,
            )  # Imported locally as live preview is optional

            preview_update.send(sender=HeadlessPreviewMixin, token=token)
        else:
            PagePreview.garbage_collect()
            page_preview = self.create_page_preview()
            page_preview.save()

        response_token = token or page_preview.token

        response = render(
            request,
            "wagtail_headless_preview/preview.html",
            {"preview_url": self.get_preview_url(response_token)},
        )

        if use_live_preview:
            # Set cookie that auto-expires after 5mins
            response.set_cookie(key="used-token", value=response_token, max_age=300)

        return response

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
