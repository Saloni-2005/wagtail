from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.staticfiles.finders import get_finders
import os
import shutil


class Command(BaseCommand):
    help = 'Fix missing static files by ensuring all Wagtail static files are properly collected'

    def handle(self, *args, **options):
        self.stdout.write('=== Fixing Missing Static Files ===')
        
        # Check for missing critical files
        self.check_missing_files()
        
        # Try to find and copy missing files
        self.find_and_copy_missing_files()
        
        self.stdout.write(self.style.SUCCESS('Static files fix completed'))

    def check_missing_files(self):
        """Check for commonly missing static files"""
        self.stdout.write('\n--- Checking for Missing Files ---')
        
        critical_files = [
            'wagtailembeds/js/embed-chooser-modal.js',
            'wagtailadmin/images/icons/radio-full.svg',
            'wagtailadmin/js/vendor/jquery-3.6.0.min.js',
            'wagtailadmin/js/vendor/tag-it.js',
        ]
        
        staticfiles_root = settings.STATIC_ROOT
        missing_files = []
        
        for file_path in critical_files:
            full_path = os.path.join(staticfiles_root, file_path)
            if not os.path.exists(full_path):
                missing_files.append(file_path)
                self.stdout.write(self.style.WARNING(f'✗ Missing: {file_path}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'✓ Found: {file_path}'))
        
        if missing_files:
            self.stdout.write(f'\nFound {len(missing_files)} missing files')
            return missing_files
        else:
            self.stdout.write(self.style.SUCCESS('All critical files found'))
            return []

    def find_and_copy_missing_files(self):
        """Use Django's static file finders to locate and copy missing files"""
        self.stdout.write('\n--- Finding and Copying Missing Files ---')
        
        try:
            # Get all static file finders
            finders = get_finders()
            
            # Files we need to ensure exist
            required_files = [
                'wagtailembeds/js/embed-chooser-modal.js',
                'wagtailadmin/images/icons/radio-full.svg',
                'wagtailadmin/js/vendor/jquery-3.6.0.min.js',
                'wagtailadmin/js/vendor/tag-it.js',
                'wagtailadmin/js/vendor/jquery-ui-1.13.2.min.js',
                'wagtailadmin/js/vendor/jquery.datetimepicker.js',
                'wagtailadmin/js/vendor/bootstrap-modal.js',
                'wagtailadmin/js/vendor/bootstrap-transition.js',
            ]
            
            for file_path in required_files:
                self.copy_file_if_missing(file_path, finders)
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error in find_and_copy: {e}'))

    def copy_file_if_missing(self, file_path, finders):
        """Copy a file if it's missing from STATIC_ROOT"""
        staticfiles_root = settings.STATIC_ROOT
        target_path = os.path.join(staticfiles_root, file_path)
        
        # Check if file already exists
        if os.path.exists(target_path):
            return
        
        # Try to find the file using Django's finders
        for finder in finders:
            try:
                found_path = finder.find(file_path)
                if found_path and os.path.exists(found_path):
                    # Create target directory if it doesn't exist
                    target_dir = os.path.dirname(target_path)
                    os.makedirs(target_dir, exist_ok=True)
                    
                    # Copy the file
                    shutil.copy2(found_path, target_path)
                    self.stdout.write(self.style.SUCCESS(f'✓ Copied: {file_path}'))
                    return
            except Exception as e:
                continue
        
        # If we get here, the file wasn't found
        self.stdout.write(self.style.WARNING(f'⚠ Could not find: {file_path}'))

    def create_missing_directories(self):
        """Create any missing directories in STATIC_ROOT"""
        staticfiles_root = settings.STATIC_ROOT
        
        required_dirs = [
            'wagtailembeds/js',
            'wagtailadmin/images/icons',
            'wagtailadmin/js/vendor',
        ]
        
        for dir_path in required_dirs:
            full_dir_path = os.path.join(staticfiles_root, dir_path)
            os.makedirs(full_dir_path, exist_ok=True)