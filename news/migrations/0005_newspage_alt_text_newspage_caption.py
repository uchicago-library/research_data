# Generated by Django 5.0.9 on 2024-12-10 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0004_alter_newslistingsettings_paginate_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="newspage",
            name="alt_text",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="newspage",
            name="caption",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]