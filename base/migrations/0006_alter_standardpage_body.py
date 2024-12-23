# Generated by Django 5.0.9 on 2024-12-20 19:25

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0005_alter_standardpage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="standardpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("paragraph", 0),
                    ("h2", 1),
                    ("h3", 2),
                    ("h4", 3),
                    ("h5", 4),
                    ("image_link", 11),
                ],
                blank=True,
                block_lookup={
                    0: ("wagtail.blocks.RichTextBlock", (), {}),
                    1: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"icon": "title", "template": "base/blocks/h2.html"},
                    ),
                    2: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"icon": "title", "template": "base/blocks/h3.html"},
                    ),
                    3: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"icon": "title", "template": "base/blocks/h4.html"},
                    ),
                    4: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"icon": "title", "template": "base/blocks/h5.html"},
                    ),
                    5: (
                        "wagtail.images.blocks.ImageChooserBlock",
                        (),
                        {"required": False},
                    ),
                    6: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Required if no link text supplied for ADA compliance",
                            "required": False,
                        },
                    ),
                    7: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Text to display below the image",
                            "required": False,
                        },
                    ),
                    8: ("wagtail.blocks.PageChooserBlock", (), {"required": False}),
                    9: (
                        "wagtail.documents.blocks.DocumentChooserBlock",
                        (),
                        {"required": False},
                    ),
                    10: ("wagtail.blocks.URLBlock", (), {"required": False}),
                    11: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("link_image", 5),
                                ("alt_text", 6),
                                ("link_text", 7),
                                ("link_page", 8),
                                ("link_document", 9),
                                ("link_external", 10),
                            ]
                        ],
                        {
                            "group": "Links",
                            "help_text": "A fancy link made out of a thumbnail and simple text. It will link to either the page, the document, or to the external, depending on the first to be non-empty.",
                            "label": "Linked Image",
                        },
                    ),
                },
            ),
        ),
    ]