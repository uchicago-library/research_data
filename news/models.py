from base.models import AbstractBasePage
from django.core.paginator import Paginator
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField


@register_setting
class NewsListingSettings(BaseSiteSetting):
    paginate_by = models.PositiveSmallIntegerField(
        null=True, blank=True, help_text="Defaults to 5 when not set."
    )

    panels = [
        FieldPanel('paginate_by'),
    ]


class NewsIndexPage(AbstractBasePage):
    subpage_types = ['news.NewsPage']

    def get_context(self, request):
        context = super().get_context(request)

        child_pages = self.get_children().live().specific()

        news_listing_settings = NewsListingSettings.for_request(request=request)

        num_items = 5
        if news_listing_settings.paginate_by:
            num_items = news_listing_settings.paginate_by

        paginator = Paginator(child_pages, num_items)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        return context


class NewsPage(AbstractBasePage):
    excerpt = RichTextField(
        blank=True, 
        features=['bold', 'italic', 'link'],
        help_text="Text to display on the news index page. Defaults to a truncation of the body.",
    )
    thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Image to display for the story. Alt text is defined when editing the image itself.",
    )
    thumbnail_caption = models.CharField(max_length=100, blank=True)
    content_panels = (
        AbstractBasePage.content_panels[:1] + 
        [
            FieldPanel('excerpt'),
            MultiFieldPanel(
                [
                    FieldPanel('thumbnail'),
                    FieldPanel('thumbnail_caption'),
                ],
                heading='Thumbnail',
            ),
        ] + 
        AbstractBasePage.content_panels[1:]
    )