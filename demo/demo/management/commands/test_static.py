from django.core.management.base import BaseCommand
from django.templatetags.static import static
from wagtail.admin.staticfiles import versioned_static


class Command(BaseCommand):
    help = 'Test static file resolution'

    def handle(self, *args, **options):
        test_files = [
            'wagtailadmin/js/vendor/jquery-3.6.0.min.js',
            'wagtailadmin/js/vendor/tag-it.js',
            'wagtailadmin/js/vendor/jquery-ui-1.13.2.min.js',
        ]
        
        for file_path in test_files:
            static_url = static(file_path)
            versioned_url = versioned_static(file_path)
            
            self.stdout.write(f"File: {file_path}")
            self.stdout.write(f"  static(): {static_url}")
            self.stdout.write(f"  versioned_static(): {versioned_url}")
            self.stdout.write("")