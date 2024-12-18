# from django.db import models
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.blocks import (
    CharBlock,
    IntegerBlock,
    PageChooserBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
)
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index


class LinkFields(models.Model):
    """
    Reusable abstract class for general links.
    """

    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.file.url
        else:
            return self.link_external

    content_panels = [
        PageChooserPanel('link_page'),
        FieldPanel('link_external'),
    ]

    class Meta:
        abstract = True


class Logo(LinkFields):
    """
    Reusable abstract class for logos.
    """

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Logo image",
    )

    content_panels = LinkFields.content_panels + [
        FieldPanel('image'),
    ]

    class Meta:
        abstract = True


@register_setting
class MainLogo(BaseGenericSetting, Logo):
    pass


@register_setting
class FooterLogo(BaseGenericSetting, Logo):
    pass


class DefaultBodyFields(StreamBlock):
    """
    Standard default streamfield options to be shared
    across content types.
    """

    paragraph = RichTextBlock()
    h2 = CharBlock(
        icon='title',
        template='base/blocks/h2.html',
    )
    h3 = CharBlock(
        icon='title',
        template='base/blocks/h3.html',
    )
    h4 = CharBlock(
        icon='title',
        template='base/blocks/h4.html',
    )
    h5 = CharBlock(
        icon='title',
        template='base/blocks/h5.html',
    )

    class Meta:
        required = False


class SectionBlock(StructBlock):
    """
    Block type for streaming in dynamic page sections.
    Will show a smattering of child pages for whatever
    parent page is selected.
    """

    heading = CharBlock(required=True, help_text='Section heading')
    page = PageChooserBlock(required=True)
    count = IntegerBlock(required=True, help_text='Number of child pages to show')

    class Meta:
        template = 'base/blocks/section_block.html'


class AbstractBasePage(Page):
    class Meta:
        abstract = True

    body = StreamField(
        DefaultBodyFields(),
        blank=True,
    )

    show_nested_children = models.BooleanField(
        default=True, help_text="Check this to display nested child pages."
    )

    nested_children_depth = models.PositiveIntegerField(
        default=1,
        help_text="Number of levels deep to show child pages (1 means immediate children only).",
    )

    content_panels = Page.content_panels + [FieldPanel('body')]
    
    show_in_menus_default = True

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]


class StandardPage(AbstractBasePage):
    # Needs to stay here, unfortunately
    from services.models import ResearchLifecyclePhase

    associated_research_lifecycle_phase = models.ForeignKey(
        ResearchLifecyclePhase,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = AbstractBasePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('show_nested_children'),
                FieldPanel('nested_children_depth'),
            ],
            heading='Dynamic Page Listing',
        ),
        FieldPanel('associated_research_lifecycle_phase'),
    ]

    def get_context(self, request):
        """
        Override the page object's get context method.
        """
        # Needs to stay here, unfortunately
        from services.models import ServicePage

        context = super(StandardPage, self).get_context(request)

        services = None
        if self.associated_research_lifecycle_phase:
            slug = self.associated_research_lifecycle_phase.slug
            filter_param = 'research_lifecycle_phase_additions__phase__slug'
            services = (
                ServicePage.objects.live().filter(**{filter_param: slug}).distinct()
            )

        context['services'] = services

        return context
