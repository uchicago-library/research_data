import os

from dev.utils import (
    populate_categories_from_xlsx,
    populate_divisions_from_xlsx,
    populate_funder_policies_from_xlsx,
    populate_research_lifecycle_phases_from_xlsx,
    populate_service_pages_from_xlsx,
)
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Populates the database with serice related snippets and pages.'

    def handle(self, *args, **kwargs):
        spreadsheet = os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            '..',
            'dev',
            'data',
            'Research_Data_Website_Services.xlsx',
        )

        research_lifecycle_phases_count = populate_research_lifecycle_phases_from_xlsx(
            spreadsheet
        )
        print(
            f'{research_lifecycle_phases_count} ResearchLifecyclePhase snippets created.'
        )

        categories_count = populate_categories_from_xlsx(spreadsheet)
        print(f'{categories_count} ServiceCategory snippets created.')

        divisions_count = populate_divisions_from_xlsx(spreadsheet)
        print(f'{divisions_count} Division snippts created.')

        funder_policies_count = populate_funder_policies_from_xlsx(spreadsheet)
        print(f'{funder_policies_count} FunderPolicy snipptes created.')

        service_pages_count = populate_service_pages_from_xlsx(spreadsheet)
        print(f'{service_pages_count} ServicePages created.')

        self.stdout.write(
            self.style.SUCCESS(
                'All service related snippets and pages have been created!'
            )
        )
