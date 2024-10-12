from django.db import models
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from .blocks import HomePageStreamBlock


class HomePage(Page):
    max_count = 1

    body = StreamField(
        HomePageStreamBlock(),
        blank=True,
        collapsed=True,
    )


    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]