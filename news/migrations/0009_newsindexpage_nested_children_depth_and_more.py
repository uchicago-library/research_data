# Generated by Django 5.0.9 on 2024-12-12 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0008_alter_newspage_excerpt_alter_newspage_thumbnail"),
    ]

    operations = [
        migrations.AddField(
            model_name="newsindexpage",
            name="nested_children_depth",
            field=models.PositiveIntegerField(
                default=1,
                help_text="Number of levels deep to show child pages (1 means immediate children only).",
            ),
        ),
        migrations.AddField(
            model_name="newsindexpage",
            name="show_nested_children",
            field=models.BooleanField(
                default=False, help_text="Check this to display nested child pages."
            ),
        ),
        migrations.AddField(
            model_name="newspage",
            name="nested_children_depth",
            field=models.PositiveIntegerField(
                default=1,
                help_text="Number of levels deep to show child pages (1 means immediate children only).",
            ),
        ),
        migrations.AddField(
            model_name="newspage",
            name="show_nested_children",
            field=models.BooleanField(
                default=False, help_text="Check this to display nested child pages."
            ),
        ),
    ]