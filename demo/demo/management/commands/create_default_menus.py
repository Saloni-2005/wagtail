from django.core.management.base import BaseCommand
from wagtail.contrib.navigation.models import Menu, MenuItem
from wagtail.models import Page
from home.models import HomePage
import json


class Command(BaseCommand):
    help = 'Creates default header and footer menus if they do not exist'

    def handle(self, *args, **options):
        try:
            self.create_header_menu()
            self.create_footer_menu()
            self.stdout.write(self.style.SUCCESS('Successfully created default menus'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating menus: {e}'))

    def create_header_menu(self):
        """Create a default header menu with custom header links"""
        header_menu, created = Menu.objects.get_or_create(
            slug='header',
            defaults={
                'title': 'Header Menu',
            }
        )
        
        if created:
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

    def create_footer_menu(self):
        """Create a default footer menu with custom footer links"""
        footer_menu, created = Menu.objects.get_or_create(
            slug='footer',
            defaults={
                'title': 'Footer Menu',
            }
        )
        
        if created:
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