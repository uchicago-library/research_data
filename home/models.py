from base.models import AbstractBasePage, SectionBlock
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField


class HomePage(AbstractBasePage):
    subpage_types = ['base.StandardPage', 'news.NewsIndexPage']

    cta_heading = models.CharField(max_length=100, blank=True)
    cta_text = RichTextField(blank=True, features=['bold'])
    cta_button_text = models.CharField(max_length=100, blank=True)
    cta_button_link = models.URLField(
        blank=True,
        help_text="Overrides the page link.",
    )
    cta_button_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
        help_text="Link to apply to the button. Link to internal pages using this, or override it with the Button Link for external links.",
    )
    cta_background_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Image to display as a background for the Call to Action. Mind the contrast, and for different screen sizes.",
    )
    sections = StreamField(
        [
            ('section', SectionBlock()),
        ],
        blank=True,
    )

    content_panels = (
        AbstractBasePage.content_panels[:1]
        + [
            MultiFieldPanel(
                [
                    FieldPanel('cta_heading'),
                    FieldPanel('cta_text'),
                    FieldPanel('cta_button_text'),
                    FieldPanel('cta_button_link'),
                    FieldPanel('cta_button_page'),
                    FieldPanel('cta_background_image'),
                ],
                heading='Call to Action Panel',
            ),
        ]
        + AbstractBasePage.content_panels[1:]
        + [
            FieldPanel('sections'),
        ]
    )

    subpage_types = [
        'base.StandardPage',
        'news.NewsIndexPage',
        'services.ServicesListingPage',
    ]
