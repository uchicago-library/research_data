from base.models import AbstractBasePage
from django.db import models
from wagtail.models import Page


class HomePage(AbstractBasePage):
    subpage_types = [
        'base.StandardPage',
        'news.NewsIndexPage',
        'services.ServicesListingPage',
    ]
