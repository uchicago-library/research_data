# Generated by Django 5.0.9 on 2024-12-10 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0005_newspage_alt_text_newspage_caption"),
    ]

    operations = [
        migrations.RenameField(
            model_name="newspage",
            old_name="alt_text",
            new_name="thumbnail_alt_text",
        ),
        migrations.RenameField(
            model_name="newspage",
            old_name="caption",
            new_name="thumbnail_caption",
        ),
    ]
