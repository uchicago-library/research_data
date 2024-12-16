# Generated by Django 5.0.9 on 2024-12-16 19:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0006_homepage_nested_children_depth_and_more"),
        ("wagtailcore", "0094_alter_page_locale"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="cta_button_page",
            field=models.ForeignKey(
                blank=True,
                help_text="Link to apply to the button. Links to internal pages, gets overriden by the Button Link for external links",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailcore.page",
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="cta_button_link",
            field=models.URLField(blank=True, help_text="Overrides the page link"),
        ),
    ]