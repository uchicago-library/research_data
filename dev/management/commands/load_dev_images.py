import os
import shutil

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Copies images from dev/images to original_images in the media directory and runs image renditions command'

    def handle(self, *args, **kwargs):
        source_dir = os.path.join(
            os.path.dirname(__file__), '..', '..', '..', 'dev', 'images'
        )
        target_dir = os.path.join(settings.MEDIA_ROOT, 'original_images')

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        for filename in os.listdir(source_dir):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                source_file = os.path.join(source_dir, filename)
                target_file = os.path.join(target_dir, filename)
                shutil.copy2(source_file, target_file)
                self.stdout.write(
                    self.style.SUCCESS(f'Copied {filename} to original_images')
                )

        call_command('wagtail_update_image_renditions')

        self.stdout.write(
            self.style.SUCCESS('Image renditions have been updated for all images.')
        )
