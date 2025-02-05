from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField

from base.models import AbstractBasePage, SectionBlock


class HomePage(AbstractBasePage):
    subpage_types = ['base.StandardPage', 'news.NewsIndexPage']

    cta_heading = models.CharField(verbose_name="Heading", max_length=100, blank=True)
    cta_text = RichTextField(verbose_name="Text", blank=True, features=['bold'])
    cta_button_text = models.CharField(
        verbose_name="Button Text", max_length=100, blank=True
    )
    cta_show_search = models.BooleanField(
        default=False,
        verbose_name="Show a services Search Bar?",
        help_text="Check this box to show a search bar inside the banner that links directly to the '/services' page. Note that a '/services' page must exist for this to work.",
    )
    cta_button_link = models.URLField(
        verbose_name="Button external link override",
        blank=True,
        help_text="Overrides the page link.",
    )
    cta_button_page = models.ForeignKey(
        'wagtailcore.Page',
        verbose_name="Button internal page link",
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
        help_text="Link to apply to the button. Link to internal pages using this, or override it with the Button Link for external links.",
    )
    cta_background_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="CTA section background image.",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Image to display as a background for the Call to Action. Mind the contrast, and for different screen sizes.",
    )
    cta_darken_image = models.BooleanField(
        default=False,
        verbose_name="Darken background image?",
        help_text="Check this box to add an overlay to the background image to darken it by 20%.",
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
                    FieldPanel('cta_show_search'),
                    FieldPanel('cta_button_text'),
                    FieldPanel('cta_button_link'),
                    FieldPanel('cta_button_page'),
                    FieldPanel('cta_background_image'),
                    FieldPanel('cta_darken_image'),
                ],
                heading='Call to Action Section (CTA)',
                help_text="Needs an image, a heading, text, or button link to be visible.",
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
