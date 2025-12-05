from django.core.management.base import BaseCommand
from wagtail.contrib.navigation.models import Menu
from django.db.models import Count


class Command(BaseCommand):
    help = 'Fix duplicate menus and add default custom header/footer to existing menus'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('🔍 DRY RUN MODE - No changes will be made'))
        
        self.fix_duplicates(dry_run)
        self.add_missing_defaults(dry_run)
        
        if not dry_run:
            self.stdout.write(self.style.SUCCESS('✅ Menu fixes completed'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ Dry run completed'))

    def fix_duplicates(self, dry_run=False):
        """Remove duplicate menus keeping only the first one of each slug"""
        self.stdout.write('🔍 Checking for duplicate menus...')
        
        # Find all duplicate slugs
        duplicate_slugs = Menu.objects.values('slug').annotate(
            count=Count('slug')
        ).filter(count__gt=1)
        
        total_removed = 0
        
        for item in duplicate_slugs:
            slug = item['slug']
            count = item['count']
            
            menus = Menu.objects.filter(slug=slug).order_by('id')
            duplicates = menus[1:]  # Keep the first one
            
            self.stdout.write(f'  Found {count} menus with slug "{slug}"')
            
            if not dry_run:
                duplicate_count = duplicates.count()
                duplicates.delete()
                total_removed += duplicate_count
                self.stdout.write(f'    ✅ Removed {duplicate_count} duplicates')
            else:
                self.stdout.write(f'    🔍 Would remove {duplicates.count()} duplicates')
        
        if not duplicate_slugs:
            self.stdout.write('  ✅ No duplicate menus found')
        elif not dry_run:
            self.stdout.write(f'  ✅ Total duplicates removed: {total_removed}')

    def add_missing_defaults(self, dry_run=False):
        """Add default custom header/footer to menus that don't have them"""
        self.stdout.write('🔍 Checking for menus missing default custom links...')
        
        # Default custom header links
        default_header_links = [
            {
                "type": "link",
                "value": {
                    "link_type": "about",
                    "title": "",
                    "url": "",
                    "page": None,
                    "open_in_new_tab": False
                }
            },
            {
                "type": "link", 
                "value": {
                    "link_type": "contact",
                    "title": "",
                    "url": "",
                    "page": None,
                    "open_in_new_tab": False
                }
            }
        ]
        
        # Default custom footer links
        default_footer_links = [
            {
                "type": "link",
                "value": {
                    "link_type": "privacy",
                    "title": "",
                    "url": "",
                    "page": None,
                    "open_in_new_tab": False
                }
            },
            {
                "type": "link",
                "value": {
                    "link_type": "terms", 
                    "title": "",
                    "url": "",
                    "page": None,
                    "open_in_new_tab": False
                }
            }
        ]
        
        updated_count = 0
        
        for menu in Menu.objects.all():
            needs_update = False
            
            # Check if custom_header is empty or None
            if not menu.custom_header:
                self.stdout.write(f'  Menu "{menu.title}" missing custom header')
                if not dry_run:
                    menu.custom_header = default_header_links
                    needs_update = True
                else:
                    self.stdout.write(f'    🔍 Would add default header links')
            
            # Check if custom_footer is empty or None
            if not menu.custom_footer:
                self.stdout.write(f'  Menu "{menu.title}" missing custom footer')
                if not dry_run:
                    menu.custom_footer = default_footer_links
                    needs_update = True
                else:
                    self.stdout.write(f'    🔍 Would add default footer links')
            
            if needs_update and not dry_run:
                try:
                    menu.save()
                    updated_count += 1
                    self.stdout.write(f'    ✅ Updated menu "{menu.title}"')
                except Exception as e:
                    self.stdout.write(f'    ❌ Failed to update menu "{menu.title}": {e}')
        
        if updated_count == 0 and not dry_run:
            self.stdout.write('  ✅ All menus already have custom links')
        elif not dry_run:
            self.stdout.write(f'  ✅ Updated {updated_count} menus with default custom links')