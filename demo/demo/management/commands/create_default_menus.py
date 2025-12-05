from django.core.management.base import BaseCommand
from wagtail.contrib.navigation.models import Menu, MenuItem
from wagtail.models import Page
from home.models import HomePage
import json


class Command(BaseCommand):
    help = 'Creates default header and footer menus if they do not exist'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreation of menus even if they exist',
        )
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Remove duplicate menus before creating defaults',
        )

    def handle(self, *args, **options):
        try:
            if options['clean']:
                self.clean_duplicate_menus()
            
            self.create_header_menu(force=options['force'])
            self.create_footer_menu(force=options['force'])
            self.stdout.write(self.style.SUCCESS('Successfully created default menus'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating menus: {e}'))

    def clean_duplicate_menus(self):
        """Remove duplicate menus keeping only the first one of each slug"""
        self.stdout.write('🧹 Cleaning duplicate menus...')
        
        # Find duplicate header menus
        header_menus = Menu.objects.filter(slug='header').order_by('id')
        if header_menus.count() > 1:
            duplicates = header_menus[1:]  # Keep the first one
            count = duplicates.count()
            duplicates.delete()
            self.stdout.write(f'  Removed {count} duplicate header menus')
        
        # Find duplicate footer menus
        footer_menus = Menu.objects.filter(slug='footer').order_by('id')
        if footer_menus.count() > 1:
            duplicates = footer_menus[1:]  # Keep the first one
            count = duplicates.count()
            duplicates.delete()
            self.stdout.write(f'  Removed {count} duplicate footer menus')
        
        # Find any other duplicate slugs
        from django.db.models import Count
        duplicate_slugs = Menu.objects.values('slug').annotate(
            count=Count('slug')
        ).filter(count__gt=1)
        
        for item in duplicate_slugs:
            slug = item['slug']
            if slug not in ['header', 'footer']:  # Already handled above
                menus = Menu.objects.filter(slug=slug).order_by('id')
                duplicates = menus[1:]
                count = duplicates.count()
                duplicates.delete()
                self.stdout.write(f'  Removed {count} duplicate "{slug}" menus')

    def create_header_menu(self, force=False):
        """Create a default header menu with custom header links"""
        header_menu, created = Menu.objects.get_or_create(
            slug='header',
            defaults={
                'title': 'Header Menu',
            }
        )
        
        if created or force:
            if force and not created:
                self.stdout.write(f'Force updating header menu: {header_menu.title}')
                # Clear existing items if forcing
                header_menu.menu_items.all().delete()
            else:
                self.stdout.write(f'Created header menu: {header_menu.title}')
            
            # Add default header menu items
            header_items = [
                {'title': 'Home', 'item_type': 'custom', 'link_url': '/'},
                {'title': 'About', 'item_type': 'about'},
                {'title': 'Services', 'item_type': 'services'},
                {'title': 'Contact', 'item_type': 'contact'},
            ]
            
            for i, item_data in enumerate(header_items):
                MenuItem.objects.create(
                    menu=header_menu,
                    sort_order=i,
                    **item_data
                )
                self.stdout.write(f'  Added menu item: {item_data["title"]}')
            
            # Add default custom header links (StreamField)
            try:
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
                header_menu.custom_header = json.dumps(default_header_links)
                header_menu.save()
                self.stdout.write('  Added default custom header links')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  Could not add custom header links: {e}'))
                
        else:
            self.stdout.write(f'Header menu already exists: {header_menu.title}')

    def create_footer_menu(self, force=False):
        """Create a default footer menu with custom footer links"""
        footer_menu, created = Menu.objects.get_or_create(
            slug='footer',
            defaults={
                'title': 'Footer Menu',
            }
        )
        
        if created or force:
            if force and not created:
                self.stdout.write(f'Force updating footer menu: {footer_menu.title}')
                # Clear existing items if forcing
                footer_menu.menu_items.all().delete()
            else:
                self.stdout.write(f'Created footer menu: {footer_menu.title}')
            
            # Add default footer menu items
            footer_items = [
                {'title': 'Privacy Policy', 'item_type': 'privacy'},
                {'title': 'Terms of Service', 'item_type': 'terms'},
                {'title': 'FAQ', 'item_type': 'faq'},
                {'title': 'Contact', 'item_type': 'contact'},
            ]
            
            for i, item_data in enumerate(footer_items):
                MenuItem.objects.create(
                    menu=footer_menu,
                    sort_order=i,
                    **item_data
                )
                self.stdout.write(f'  Added menu item: {item_data["title"]}')
            
            # Add default custom footer links (StreamField)
            try:
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
                footer_menu.custom_footer = json.dumps(default_footer_links)
                footer_menu.save()
                self.stdout.write('  Added default custom footer links')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  Could not add custom footer links: {e}'))
                
        else:
            self.stdout.write(f'Footer menu already exists: {footer_menu.title}')