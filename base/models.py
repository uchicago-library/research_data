from django.db import models
from wagtail.admin.panels import FieldPanel, HelpPanel, MultiFieldPanel, PageChooserPanel
from wagtail.blocks import (
    CharBlock,
    IntegerBlock,
    PageChooserBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    URLBlock,
)
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
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


class ImageLink(StructBlock):
    """
    Normal image for web exhibits.
    """

    link_image = ImageChooserBlock(required=False)
    alt_text = CharBlock(
        required=False,
        help_text='Required if no link text supplied for ADA compliance',
    )
    link_text = CharBlock(
        required=False,
        help_text='Text to display below the image',
    )
    link_page = PageChooserBlock(required=False)
    link_document = DocumentChooserBlock(required=False)
    link_external = URLBlock(required=False)

    # Define the order of fields in the admin interface
    content_panels = [
        FieldPanel('link_image'),
        FieldPanel('alt_text'),
        FieldPanel('link_text'),
        FieldPanel('link_page'),
        FieldPanel('link_document'),
        FieldPanel('link_external'),
    ]

    class Meta:
        icon = 'image'
        template = 'base/blocks/image_link.html'


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


class FloatingButton(LinkFields):
    """
    Reusable abstract class a floating button.
    Originally made for a feedback survey link.
    """

    text = models.CharField(
        max_length=255, blank=True, help_text="Text to display on the button"
    )

    content_panels = LinkFields.content_panels + [
        FieldPanel('text'),
    ]

    class Meta:
        abstract = True


@register_setting(icon='image')
class MainLogo(BaseGenericSetting, Logo):
    pass


@register_setting(icon='image')
class FooterLogo(BaseGenericSetting, Logo):
    pass


@register_setting(icon='comment')
class FloatingFooterButton(BaseGenericSetting, FloatingButton):
    pass


@register_setting(icon='rotate')
class InteractiveDiagram(BaseGenericSetting):
    """
    Settings for the interactive diagram displayed on pages.
    This diagram represents the research data lifecycle with 7 phases.
    """

    title = models.CharField(
        max_length=255,
        default="Research Data Lifecycle",
        help_text="Mandatory title for accessibility purposes. This will be read by screen readers.",
    )

    description = models.TextField(
        default="""This diagram represents a continuous research data lifecycle composed of seven sequential phases arranged in a circle, 
        while the seventh phase is centered within the circle and present throughout.
        Each wedge is a button that leads to a detailed page for that phase. 
        The circular layout communicates that once the final phase is reached, the process loops back to the first.
        """,
        help_text="Mandatory description for accessibility purposes. This will be read by screen readers. "
        "Describe the purpose and meaning of the diagram's visual concepts.",
    )

    font_size = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=14.0,
        help_text="Font size for diagram text in pixels. Recommended range: 10.0 to 18.0, but any value is allowed.",
    )

    # Phase 1: Plan and Design
    phase1_text = models.CharField(
        max_length=100,
        default="Plan & Design",
    )
    phase1_link = models.CharField(
        max_length=255,
        default="/research-lifecycle/plan-design/",
    )
    phase1_fill_color = models.CharField(
        max_length=7,
        default="#800000",
    )
    phase1_text_color = models.CharField(
        max_length=7,
        default="#ffffff",
    )

    # Phase 2: Collect and Create
    phase2_text = models.CharField(
        max_length=100,
        default="Collect & Create",
    )
    phase2_link = models.CharField(
        max_length=255,
        default="/research-lifecycle/collect-create/",
    )
    phase2_fill_color = models.CharField(
        max_length=7,
        default="#a9431e",
    )
    phase2_text_color = models.CharField(
        max_length=7,
        default="#ffffff",
    )

    # Phase 3: Analyze and Collaborate
    phase3_text = models.CharField(
        max_length=100,
        default="Analyze & Collaborate",
    )
    phase3_link = models.CharField(
        max_length=255,
        default="/research-lifecycle/analyze-collaborate/",
    )
    phase3_fill_color = models.CharField(
        max_length=7,
        default="#404040",
    )
    phase3_text_color = models.CharField(
        max_length=7,
        default="#ffffff",
    )

    # Phase 4: Evaluate and Archive
    phase4_text = models.CharField(
        max_length=100,
        default="Evaluate & Archive",
    )
    phase4_link = models.CharField(
        max_length=255,
        default="/research-lifecycle/evaluate-archive/",
    )
    phase4_fill_color = models.CharField(
        max_length=7,
        default="#a9431e",
    )
    phase4_text_color = models.CharField(
        max_length=7,
        default="#ffffff",
    )

    # Phase 5: Share
    phase5_text = models.CharField(
        max_length=100,
        default="Share",
    )
    phase5_link = models.CharField(
        max_length=255,
        default="/research-lifecycle/share/",
    )
    phase5_fill_color = models.CharField(
        max_length=7,
        default="#404040",
    )
    phase5_text_color = models.CharField(
        max_length=7,
        default="#ffffff",
    )

    # Phase 6: Publish and Reuse
    phase6_text = models.CharField(
        max_length=100,
        default="Publish & Reuse",
    )
    phase6_link = models.CharField(
        max_length=255,
        default="/research-lifecycle/publish-reuse/",
    )
    phase6_fill_color = models.CharField(
        max_length=7,
        default="#a9431e",
    )
    phase6_text_color = models.CharField(
        max_length=7,
        default="#ffffff",
    )

    # Phase 7: Store and Manage
    phase7_text = models.CharField(
        max_length=100,
        default="Store & Manage",
    )
    phase7_link = models.CharField(
        max_length=255,
        default="/research-lifecycle/store-manage/",
    )
    phase7_fill_color = models.CharField(
        max_length=7,
        default="#d9d9d9",
    )
    phase7_text_color = models.CharField(
        max_length=7,
        default="#000000",
    )

    panels = [
        HelpPanel(
            content='This page allows to customize the interactive research data lifecycle diagram. <br>'
                'This can be shown on the home page or on any standard page by checking the "Show Interactive Diagram" box. <br>'
                'The diagram is made up of seven shapes and cannot be changed in number or shape. <br>'
                '<br>'
                'Some customization is possible through the fields below, but test them thoroughly for readability and accessibility, including the hover effect. '
                'The default colors are chosen for good contrast, and to be distinguishible for color-blind users. '
                'Each phase below has four fields: <br>'
                      '<strong>Text</strong> - Keep short to fit in the diagram box. <br>'
                      '<strong>Link</strong> - Format as /path/to/page/ for internal links or https://example.com for external links. <br>'
                      '<strong>Fill Color</strong> - Hex color code for the shape background (e.g., #800000 for maroon). <br>'
                      '<strong>Text Color</strong> - Hex color code for the text (e.g., #ffffff for white).',
        ),
        MultiFieldPanel(
            [
                FieldPanel('title'),
                FieldPanel('description'),
            ],
            heading='Accessibility Settings (Required)',
        ),
        FieldPanel('font_size'),
        MultiFieldPanel(
            [
                FieldPanel('phase1_text'),
                FieldPanel('phase1_link'),
                FieldPanel('phase1_fill_color'),
                FieldPanel('phase1_text_color'),
            ],
            heading='Phase 1',
            help_text='Defaults: Plan & Design | /research-lifecycle/plan-design/ | #800000 | #ffffff',
        ),
        MultiFieldPanel(
            [
                FieldPanel('phase2_text'),
                FieldPanel('phase2_link'),
                FieldPanel('phase2_fill_color'),
                FieldPanel('phase2_text_color'),
            ],
            heading='Phase 2',
            help_text='Defaults: Collect & Create | /research-lifecycle/collect-create/ | #a9431e | #ffffff',
        ),
        MultiFieldPanel(
            [
                FieldPanel('phase3_text'),
                FieldPanel('phase3_link'),
                FieldPanel('phase3_fill_color'),
                FieldPanel('phase3_text_color'),
            ],
            heading='Phase 3',
            help_text='Defaults: Analyze & Collaborate | /research-lifecycle/analyze-collaborate/ | #404040 | #ffffff',
        ),
        MultiFieldPanel(
            [
                FieldPanel('phase4_text'),
                FieldPanel('phase4_link'),
                FieldPanel('phase4_fill_color'),
                FieldPanel('phase4_text_color'),
            ],
            heading='Phase 4',
            help_text='Defaults: Evaluate & Archive | /research-lifecycle/evaluate-archive/ | #a9431e | #ffffff',
        ),
        MultiFieldPanel(
            [
                FieldPanel('phase5_text'),
                FieldPanel('phase5_link'),
                FieldPanel('phase5_fill_color'),
                FieldPanel('phase5_text_color'),
            ],
            heading='Phase 5',
            help_text='Defaults: Share | /research-lifecycle/share/ | #404040 | #ffffff',
        ),
        MultiFieldPanel(
            [
                FieldPanel('phase6_text'),
                FieldPanel('phase6_link'),
                FieldPanel('phase6_fill_color'),
                FieldPanel('phase6_text_color'),
            ],
            heading='Phase 6',
            help_text='Defaults: Publish & Reuse | /research-lifecycle/publish-reuse/ | #a9431e | #ffffff',
        ),
        MultiFieldPanel(
            [
                FieldPanel('phase7_text'),
                FieldPanel('phase7_link'),
                FieldPanel('phase7_fill_color'),
                FieldPanel('phase7_text_color'),
            ],
            heading='Phase 7 (center)',
            help_text='Defaults: Store & Manage | /research-lifecycle/store-manage/ | #d9d9d9 | #000000',
        ),
    ]

    class Meta:
        verbose_name = "Interactive Diagram Settings"
        verbose_name_plural = "Interactive Diagram Settings"


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

    image_link = ImageLink(
        label="Linked Image",
        help_text='A fancy link made out of a thumbnail and simple text. It will link to either the page, the document, or to the external, depending on the first to be non-empty.',
        group="Links",
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

    show_interactive_diagram = models.BooleanField(
        default=False,
        verbose_name="Show Interactive Diagram",
        help_text="Check this box to display the interactive research data lifecycle diagram on this page. "
        "The diagram is customizable in Settings > Interactive Diagram Settings. "
        "This interactive diagram provides an accessible, visual representation of the research lifecycle phases.",
    )

    content_panels = (
        AbstractBasePage.content_panels[:1]
        + [ FieldPanel('show_interactive_diagram', icon='rotate'), ]
        + AbstractBasePage.content_panels[1:]
        + [ MultiFieldPanel(
            [
                FieldPanel('show_nested_children'),
                FieldPanel('nested_children_depth'),
            ],
            heading='Dynamic Page Listing',
        ),]
        + [ FieldPanel('associated_research_lifecycle_phase'), ]
    )

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
