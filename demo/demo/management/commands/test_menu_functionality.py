from django.core.management.base import BaseCommand
from wagtail.contrib.navigation.models import Menu, MenuItem
import json


class Command(BaseCommand):
    help = 'Test menu functionality including custom header/footer saving'

    def handle(self, *args, **options):
        self.stdout.write('=== Testing Menu Functionality ===')
        
        # Test 1: Create a test menu
        self.test_menu_creation()
        
        # Test 2: Test custom header saving
        self.test_custom_header_saving()
        
        # Test 3: Test custom footer saving  
        self.test_custom_footer_saving()
        
        self.stdout.write(self.style.SUCCESS('All menu tests completed'))

    def test_menu_creation(self):
        """Test basic menu creation"""
        self.stdout.write('\n--- Test 1: Menu Creation ---')
        
        try:
            test_menu = Menu.objects.create(
                title='Test Menu',
                slug='test-menu'
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Created test menu: {test_menu.title}'))
            
            # Add a menu item
            MenuItem.objects.create(
                menu=test_menu,
                title='Test Item',
                item_type='custom',
                content='Test content'
            )
            self.stdout.write(self.style.SUCCESS('✓ Added test menu item'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Menu creation failed: {e}'))

    def test_custom_header_saving(self):
        """Test custom header StreamField saving"""
        self.stdout.write('\n--- Test 2: Custom Header Saving ---')
        
        try:
            # Get or create a test menu
            menu, created = Menu.objects.get_or_create(
                slug='header-test',
                defaults={'title': 'Header Test Menu'}
            )
            
            # Test simple custom header data
            header_data = [
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
                        "link_type": "custom",
                        "title": "Custom Link",
                        "url": "https://example.com",
                        "page": None,
                        "open_in_new_tab": True
                    }
                }
            ]
            
            # Try to save the custom header
            menu.custom_header = json.dumps(header_data)
            menu.save()
            
            # Verify it was saved
            menu.refresh_from_db()
            if menu.custom_header:
                self.stdout.write(self.style.SUCCESS('✓ Custom header saved successfully'))
                self.stdout.write(f'  Header data: {menu.custom_header}')
            else:
                self.stdout.write(self.style.WARNING('⚠ Custom header appears empty after save'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Custom header saving failed: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())

    def test_custom_footer_saving(self):
        """Test custom footer StreamField saving"""
        self.stdout.write('\n--- Test 3: Custom Footer Saving ---')
        
        try:
            # Get or create a test menu
            menu, created = Menu.objects.get_or_create(
                slug='footer-test',
                defaults={'title': 'Footer Test Menu'}
            )
            
            # Test simple custom footer data
            footer_data = [
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
                        "link_type": "custom",
                        "title": "Support",
                        "url": "/support/",
                        "page": None,
                        "open_in_new_tab": False
                    }
                }
            ]
            
            # Try to save the custom footer
            menu.custom_footer = json.dumps(footer_data)
            menu.save()
            
            # Verify it was saved
            menu.refresh_from_db()
            if menu.custom_footer:
                self.stdout.write(self.style.SUCCESS('✓ Custom footer saved successfully'))
                self.stdout.write(f'  Footer data: {menu.custom_footer}')
            else:
                self.stdout.write(self.style.WARNING('⚠ Custom footer appears empty after save'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Custom footer saving failed: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())