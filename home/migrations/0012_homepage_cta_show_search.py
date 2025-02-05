# Generated by Django 5.0.9 on 2025-02-05 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0011_alter_homepage_body"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="cta_show_search",
            field=models.BooleanField(
                default=False,
                help_text="Check this box to show a search bar inside the banner that links directly to the '/services' page. Note that a '/services' page must exist for this to work.",
                verbose_name="Show a services Search Bar?",
            ),
        ),
    ]
