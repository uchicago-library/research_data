from base.models import AbstractBasePage
from django.db import models
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.models import Orderable
from wagtail.search.utils import parse_query_string
from wagtail.snippets.models import register_snippet


@register_snippet
class ServiceCategory(models.Model):

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    panels = [
        FieldPanel('name'),
    ]

    class Meta:
        verbose_name = 'Service Category'
        verbose_name_plural = 'Service Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ServiceCategoryAddition(Orderable, models.Model):
    page = ParentalKey(
        'services.ServicePage',
        on_delete=models.CASCADE,
        related_name='service_category_additions',
    )
    category = models.ForeignKey(
        'services.ServiceCategory', on_delete=models.CASCADE, related_name='+'
    )

    class Meta(Orderable.Meta):
        verbose_name = 'Service Category Addition'
        verbose_name_plural = 'Service Category Additions'

    panels = [
        FieldPanel('category'),
    ]

    def __str__(self):
        return self.page.title + " -> " + self.category.name


@register_snippet
class ResearchLifecyclePhase(models.Model):

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    panels = [
        FieldPanel('name'),
    ]

    class Meta:
        verbose_name = 'Research Lifecycle Phase'
        verbose_name_plural = 'Research Lifecycle Phases'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ResearchLifecyclePhaseAddition(Orderable, models.Model):
    page = ParentalKey(
        'services.ServicePage',
        on_delete=models.CASCADE,
        related_name='research_lifecycle_phase_additions',
    )
    phase = models.ForeignKey(
        'services.ResearchLifecyclePhase', on_delete=models.CASCADE, related_name='+'
    )

    class Meta(Orderable.Meta):
        verbose_name = 'Research Lifecycle Phase Addition'
        verbose_name_plural = 'Research Lifecycle Phase Additions'

    panels = [
        FieldPanel('phase'),
    ]

    def __str__(self):
        return self.page.title + " -> " + self.phase.name


@register_snippet
class Division(models.Model):

    name = models.CharField(max_length=255, unique=True)
    url = models.URLField(verbose_name='URL', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ServicePageDivisionAddition(Orderable, models.Model):
    page = ParentalKey(
        'services.ServicePage',
        on_delete=models.CASCADE,
        related_name='division_additions',
    )
    division = models.ForeignKey(
        'services.Division', on_delete=models.CASCADE, related_name='+'
    )

    class Meta(Orderable.Meta):
        verbose_name = 'Division Addition'
        verbose_name_plural = 'Division Additions'

    panels = [
        FieldPanel('division'),
    ]

    def __str__(self):
        return self.page.title + " -> " + self.division.name


@register_snippet
class FunderPolicy(models.Model):

    name = models.CharField(max_length=255, unique=True)
    url = models.URLField(verbose_name='URL', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]

    class Meta:
        verbose_name = 'Funder Policy'
        verbose_name_plural = 'Funder Policies'
        ordering = ['name']

    def __str__(self):
        return self.name


class ServicePageFunderPolicyAddition(Orderable, models.Model):
    page = ParentalKey(
        'services.ServicePage',
        on_delete=models.CASCADE,
        related_name='funder_policy_additions',
    )
    funder_policy = models.ForeignKey(
        'services.FunderPolicy', on_delete=models.CASCADE, related_name='+'
    )

    class Meta(Orderable.Meta):
        verbose_name = 'Funder Policy Addition'
        verbose_name_plural = 'Funder Policy Additions'

    panels = [
        FieldPanel('funder_policy'),
    ]

    def __str__(self):
        return self.page.title + " -> " + self.funder_policy.name


class ServicePage(AbstractBasePage):

    service_url = models.URLField(verbose_name='URL', max_length=300, blank=True)

    content_panels = AbstractBasePage.content_panels + [
        FieldPanel('service_url'),
        InlinePanel(
            'research_lifecycle_phase_additions', label='Research Lifecycle Phases'
        ),
        InlinePanel('service_category_additions', label='Categories'),
        InlinePanel('division_additions', label='Divisions'),
        InlinePanel('funder_policy_additions', label='Funder Policies'),
    ]

    def get_context(self, request):
        """
        Override the page object's get context method.
        """
        context = super(ServicePage, self).get_context(request)

        clean_url = ''
        if self.service_url:
            clean_url = self.service_url.replace('https://', '').replace('http://', '')
            if clean_url.endswith('/'):
                clean_url = clean_url[:-1]

        context['clean_url'] = clean_url

        return context


class ServicesListingPage(RoutablePageMixin, AbstractBasePage):
    subpage_types = ['services.ServicePage']

    def filter_services(self, request, filter_param, slug=None):
        """
        Helper function to filter services based on the provided filter parameter and slug.

        Args:
            request (obj): request object.
            filter_param (str): string representing a filter parameter.
            slug (str or None): slug for a snippet.

        Returns:
            A context override for the sercies variable.

        """
        phase_map = {
            phase.slug: phase.name 
            for phase in ResearchLifecyclePhase.objects.all()
        }
        
        services = self.get_children().live().type(ServicePage).specific()

        if slug:
            slug = slug.lower()
            services = services.filter(**{filter_param: slug}).distinct()

        return self.render(
            request,
            context_overrides={
                'services': services,
                'service_filter_name': phase_map.get(slug, False),
            },
        )

    @path('category/<str:slug>/')
    @path('category/')
    def category(self, request, slug=None):
        """
        Category view.
        """
        filter_param = 'servicepage__service_category_additions__category__slug'
        return self.filter_services(request, filter_param, slug)

    @path('division/<str:slug>/')
    @path('division/')
    def division(self, request, slug=None):
        """
        Division view.
        """
        filter_param = 'servicepage__division_additions__division__slug'
        return self.filter_services(request, filter_param, slug)

    @path('funder/<str:slug>/')
    @path('funder/')
    def funder_policy(self, request, slug=None):
        """
        Funder policy view.
        """
        filter_param = 'servicepage__funder_policy_additions__funder_policy__slug'
        return self.filter_services(request, filter_param, slug)

    @path('phase/<str:slug>/')
    @path('phase/')
    def research_lifecycle_phase(self, request, slug=None):
        """
        Research lifecycle phase view.
        """
        filter_param = 'servicepage__research_lifecycle_phase_additions__phase__slug'
        return self.filter_services(request, filter_param, slug)

    def get_context(self, request):
        """
        Override the page object's get context method.
        """
        context = super(ServicesListingPage, self).get_context(request)

        services = self.get_children().live().type(ServicePage).specific()
        phases = ResearchLifecyclePhase.objects.all()

        query = request.GET.get('q')

        if query:
            query_filters, query = parse_query_string(query, operator='or')
            services = services.search(query)

        context['services'] = services
        context['phases'] = phases

        return context
