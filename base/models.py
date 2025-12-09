# from django.db import models
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


@register_setting
class MainLogo(BaseGenericSetting, Logo):
    pass


@register_setting
class FooterLogo(BaseGenericSetting, Logo):
    pass


@register_setting
class FloatingFooterButton(BaseGenericSetting, FloatingButton):
    pass


def create_diagram_phase_fields(phase_num, phase_name, default_text, default_link, default_fill, default_text_color):
    """
    Helper function to create the four fields for a diagram phase.
    Returns a dictionary of field_name: field_instance.
    """
    fields = {}
    
    fields[f'phase{phase_num}_text'] = models.CharField(
        max_length=100,
        default=default_text,
    )
    
    fields[f'phase{phase_num}_link'] = models.CharField(
        max_length=255,
        default=default_link,
    )
    
    fields[f'phase{phase_num}_fill_color'] = models.CharField(
        max_length=7,
        default=default_fill,
    )
    
    fields[f'phase{phase_num}_text_color'] = models.CharField(
        max_length=7,
        default=default_text_color,
    )
    
    return fields


# Define the 7 phases with their default values
DIAGRAM_PHASES = [
    (1, "Plan and Design", "Plan & Design", "/research-lifecycle/plan-design/", "#800000", "#ffffff"),
    (2, "Collect and Create", "Collect & Create", "/research-lifecycle/collect-create/", "#a9431e", "#ffffff"),
    (3, "Analyze and Collaborate", "Analyze & Collaborate", "/research-lifecycle/analyze-collaborate/", "#404040", "#ffffff"),
    (4, "Evaluate and Archive", "Evaluate & Archive", "/research-lifecycle/evaluate-archive/", "#a9431e", "#ffffff"),
    (5, "Share", "Share", "/research-lifecycle/share/", "#404040", "#ffffff"),
    (6, "Publish and Reuse", "Publish & Reuse", "/research-lifecycle/publish-reuse/", "#a9431e", "#ffffff"),
    (7, "Store and Manage", "Store & Manage", "/research-lifecycle/store-manage/", "#d9d9d9", "#000000"),
]


@register_setting
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
        default="The research data lifecycle represents the phases of the research data process. "
        "The research data lifecycle is one part of the overall research process, and, "
        "just as the research process is iterative, so too is the research data lifecycle: "
        "each component builds upon the next, and moving between phases is a natural part "
        "of the overall research process.",
        help_text="Mandatory description for accessibility purposes. This will be read by screen readers.",
    )

    font_size = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=14.0,
        help_text="Font size for diagram text in pixels. Recommended range: 10.0 to 18.0, but any value is allowed.",
    )

    class Meta:
        verbose_name = "Interactive Diagram Settings"
        verbose_name_plural = "Interactive Diagram Settings"


# Dynamically add phase fields to the InteractiveDiagram model
for phase_num, phase_name, default_text, default_link, default_fill, default_text_color in DIAGRAM_PHASES:
    phase_fields = create_diagram_phase_fields(phase_num, phase_name, default_text, default_link, default_fill, default_text_color)
    for field_name, field_instance in phase_fields.items():
        field_instance.contribute_to_class(InteractiveDiagram, field_name)


# Build the panels dynamically
InteractiveDiagram.panels = [
    HelpPanel(
        content='This page allows to customize the interactive research data lifecycle diagram. </br>'
            'This can be shown on the home page or on any standard page by checking the "Show Interactive Diagram" box. </br>'
            'The diagram is made up of seven shapes and cannot be changed in number or shape. </br>'
            '</br>'
            'Some customization is possible through the fields below, but test them thoroughly for readability and accessibility, including the hover effect. '
            'The default colors are chosen for good contrast, and to be distinguishible for color-blind users. '
            'Each phase below has four fields: </br>'
                  '<strong>Text</strong> - Keep short to fit in the diagram box. </br>'
                  '<strong>Link</strong> - Format as /path/to/page/ for internal links or https://example.com for external links. </br>'
                  '<strong>Fill Color</strong> - Hex color code for the shape background (e.g., #800000 for maroon). </br>'
                  '<strong>Text Color</strong> - Hex color code for the text (e.g., #ffffff for white). </br>'
                  '</br>'
                  '<strong>Default Values:</strong></br>'
                  '1. Plan & Design: /research-lifecycle/plan-design/ | #800000 | #ffffff</br>'
                  '2. Collect & Create: /research-lifecycle/collect-create/ | #a9431e | #ffffff</br>'
                  '3. Analyze & Collaborate: /research-lifecycle/analyze-collaborate/ | #404040 | #ffffff</br>'
                  '4. Evaluate & Archive: /research-lifecycle/evaluate-archive/ | #a9431e | #ffffff</br>'
                  '5. Share: /research-lifecycle/share/ | #404040 | #ffffff</br>'
                  '6. Publish & Reuse: /research-lifecycle/publish-reuse/ | #a9431e | #ffffff</br>'
                  '7. Store & Manage: /research-lifecycle/store-manage/ | #d9d9d9 | #000000',
    ),
    MultiFieldPanel(
        [
            FieldPanel('title'),
            FieldPanel('description'),
        ],
        heading='Accessibility Settings (Required)',
    ),
    FieldPanel('font_size'),
] + [
    MultiFieldPanel(
        [
            FieldPanel(f'phase{phase_num}_text'),
            FieldPanel(f'phase{phase_num}_link'),
            FieldPanel(f'phase{phase_num}_fill_color'),
            FieldPanel(f'phase{phase_num}_text_color'),
        ],
        heading=f'Phase {phase_num}: {phase_name}',
    )
    for phase_num, phase_name, _, _, _, _ in DIAGRAM_PHASES
]

# Add icon to the settings menu
InteractiveDiagram.icon = 'repeat'


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

    content_panels = AbstractBasePage.content_panels + [
        FieldPanel('show_interactive_diagram', icon='repeat'),
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
