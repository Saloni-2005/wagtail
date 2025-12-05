from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Verify the complete setup is working'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Verifying setup...'))
        
        # Check media directory
        media_dir = settings.MEDIA_ROOT
        if os.path.exists(media_dir):
            self.stdout.write(self.style.SUCCESS(f'✅ Media directory exists: {media_dir}'))
        else:
            self.stdout.write(self.style.ERROR(f'❌ Media directory missing: {media_dir}'))
        
        # Check static files
        static_root = settings.STATIC_ROOT
        if static_root and os.path.exists(static_root):
            self.stdout.write(self.style.SUCCESS(f'✅ Static files directory exists: {static_root}'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️ Static files not collected yet: {static_root}'))
        
        # Check navigation app
        if 'wagtail.contrib.navigation' in settings.INSTALLED_APPS:
            self.stdout.write(self.style.SUCCESS('✅ Navigation app installed'))
        else:
            self.stdout.write(self.style.ERROR('❌ Navigation app not installed'))
        
        # Check database tables
        from wagtail.contrib.navigation.models import Menu, MenuItem
        from django.db.models import Count
        try:
            menu_count = Menu.objects.count()
            item_count = MenuItem.objects.count()
            self.stdout.write(self.style.SUCCESS(f'✅ Database: {menu_count} menus, {item_count} menu items'))
            
            # Check for duplicate menus
            duplicate_slugs = Menu.objects.values('slug').annotate(
                count=Count('slug')
            ).filter(count__gt=1)
            
            if duplicate_slugs:
                self.stdout.write(self.style.WARNING(f'⚠️ Found duplicate menu slugs:'))
                for item in duplicate_slugs:
                    self.stdout.write(f'    - "{item["slug"]}" appears {item["count"]} times')
                self.stdout.write(self.style.WARNING('    Run: python manage.py fix_menu_duplicates'))
            else:
                self.stdout.write(self.style.SUCCESS('✅ No duplicate menus found'))
            
            # Check for menus missing custom header/footer
            menus_missing_defaults = 0
            for menu in Menu.objects.all():
                if not menu.custom_header or not menu.custom_footer:
                    menus_missing_defaults += 1
            
            if menus_missing_defaults > 0:
                self.stdout.write(self.style.WARNING(f'⚠️ {menus_missing_defaults} menus missing default custom links'))
                self.stdout.write(self.style.WARNING('    Run: python manage.py fix_menu_duplicates'))
            else:
                self.stdout.write(self.style.SUCCESS('✅ All menus have custom header/footer links'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Database error: {e}'))
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Setup verification complete!'))