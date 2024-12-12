# from django.db import models
from django.db import models
from wagtail.admin.panels import FieldPanel, PageChooserPanel
from wagtail.blocks import CharBlock, RichTextBlock, StreamBlock
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


class AbstractBasePage(Page):
    class Meta:
        abstract = True

    body = StreamField(
        DefaultBodyFields(),
        blank=True,
    )

    content_panels = Page.content_panels + [FieldPanel('body')]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]


class StandardPage(AbstractBasePage):
    pass
