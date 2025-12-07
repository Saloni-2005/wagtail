"""
Comprehensive tests for Wagtail Custom Navigation feature.
"""

import os
import django
from django.conf import settings

# Configure Django settings before importing models
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings.dev')
    django.setup()

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from wagtail.test.utils import WagtailTestUtils
from wagtail.contrib.navigation.models import Menu, MenuItem

class NavigationTestCase(TestCase, WagtailTestUtils):
    """Base test case with common setup for navigation tests."""
    
    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        
        # Create test pages using Wagtail's test utilities
        from wagtail.models import Page
        from django.contrib.contenttypes.models import ContentType
        import uuid
        
        # Get or create root page
        try:
            self.root_page = Page.objects.get(depth=1)
        except Page.DoesNotExist:
            # Create root page if it doesn't exist
            content_type = ContentType.objects.get_for_model(Page)
            self.root_page = Page.objects.create(
                title="Root",
                slug="root",
                content_type=content_type,
                path="0001",
                depth=1,
                numchild=0,
            )
        
        # Create test pages with unique slugs to avoid conflicts
        content_type = ContentType.objects.get_for_model(Page)
        unique_id = str(uuid.uuid4())[:8]
        
        self.home_page = self.root_page.add_child(instance=Page(
            title=f"Test Home {unique_id}",
            slug=f"test-home-{unique_id}",
            content_type=content_type,
        ))
        
        self.about_page = self.root_page.add_child(instance=Page(
            title=f"Test About {unique_id}",
            slug=f"test-about-{unique_id}",
            content_type=content_type,
        ))
        
        # Create test menu
        self.menu = Menu.objects.create(
            title="Test Main Menu",
            slug=f"test-main-{unique_id}",
            home_page=self.home_page
        )


class MenuCRUDTests(NavigationTestCase):
    """Test CRUD operations for Menu and MenuItem models."""
    
    def test_create_menu(self):
        """Test creating a new menu."""
        menu = Menu.objects.create(
            title="Test Menu",
            slug="test-menu",
            home_page=self.home_page
        )
        
        self.assertEqual(menu.title, "Test Menu")
        self.assertEqual(menu.slug, "test-menu")
        self.assertEqual(menu.home_page, self.home_page)
        self.assertEqual(str(menu), "Test Menu")
    
    def test_create_menu_item(self):
        """Test creating menu items with different configurations."""
        # Test predefined item type
        item1 = MenuItem.objects.create(
            menu=self.menu,
            item_type="about",
            title="About",
            slug="about",
            content="About us content"
        )
        
        # Test custom item with external URL
        item2 = MenuItem.objects.create(
            menu=self.menu,
            item_type="custom",
            title="External Link",
            slug="external",
            link_url="https://example.com",
            open_in_new_tab=True
        )
        
        # Test item with internal page
        item3 = MenuItem.objects.create(
            menu=self.menu,
            item_type="custom",
            title="Internal Page",
            slug="internal",
            link_page=self.about_page
        )
        
        self.assertEqual(item1.item_type, "about")
        self.assertEqual(item1.title, "About")
        self.assertEqual(str(item1), "About")
        
        self.assertEqual(item2.link_url, "https://example.com")
        self.assertTrue(item2.open_in_new_tab)
        
        self.assertEqual(item3.link_page, self.about_page)
    
    def test_update_menu_item(self):
        """Test updating menu item properties."""
        item = MenuItem.objects.create(
            menu=self.menu,
            item_type="contact",
            title="Contact",
            slug="contact"
        )
        
        # Update item
        item.title = "Contact Us"
        item.link_url = "https://contact.example.com"
        item.save()
        
        # Refresh from database
        item.refresh_from_db()
        
        self.assertEqual(item.title, "Contact Us")
        self.assertEqual(item.link_url, "https://contact.example.com")
    
    def test_delete_menu_item(self):
        """Test deleting menu items."""
        item = MenuItem.objects.create(
            menu=self.menu,
            item_type="services",
            title="Services",
            slug="services"
        )
        
        item_id = item.id
        item.delete()
        
        with self.assertRaises(MenuItem.DoesNotExist):
            MenuItem.objects.get(id=item_id)

class URLGenerationTests(NavigationTestCase):
    """Test URL generation for different menu item types."""
    
    def test_page_url_generation(self):
        """Test URL generation for items linked to pages."""
        item = MenuItem.objects.create(
            menu=self.menu,
            item_type="custom",
            title="About Page",
            slug="about-page",
            link_page=self.about_page
        )
        
        self.assertEqual(item.link, self.about_page.url)
    
    def test_external_url_generation(self):
        """Test URL generation for external links."""
        item = MenuItem.objects.create(
            menu=self.menu,
            item_type="custom",
            title="External",
            slug="external",
            link_url="https://example.com"
        )
        
        self.assertEqual(item.link, "https://example.com")
    
    def test_auto_generated_url(self):
        """Test auto-generated URLs for items without explicit links."""
        item = MenuItem.objects.create(
            menu=self.menu,
            item_type="about",
            title="About",
            slug="about"
        )
        
        expected_url = f"/{self.menu.slug}/{item.slug}/"
        self.assertEqual(item.link, expected_url)


class ConditionalVisibilityTests(NavigationTestCase):
    """Test conditional visibility of menu items."""
    
    def test_always_visible(self):
        """Test items that are always visible."""
        item = MenuItem.objects.create(
            menu=self.menu,
            item_type="about",
            title="About",
            slug="about",
            show_when="always"
        )
        
        # Should be visible for both authenticated and anonymous users
        self.assertTrue(item.show(authenticated=True))
        self.assertTrue(item.show(authenticated=False))
    
    def test_logged_in_only(self):
        """Test items visible only when logged in."""
        item = MenuItem.objects.create(
            menu=self.menu,
            item_type="custom",
            title="Dashboard",
            slug="dashboard",
            show_when="logged_in"
        )
        
        self.assertTrue(item.show(authenticated=True))
        self.assertFalse(item.show(authenticated=False))
    
    def test_anonymous_only(self):
        """Test items visible only when not logged in."""
        item = MenuItem.objects.create(
            menu=self.menu,
            item_type="custom",
            title="Sign Up",
            slug="signup",
            show_when="not_logged_in"
        )
        
        self.assertFalse(item.show(authenticated=True))
        self.assertTrue(item.show(authenticated=False))

if __name__ == '__main__':
    import django
    from django.conf import settings
    from django.test.utils import get_runner
    
    # Configure Django settings for standalone test execution
    if not settings.configured:
        import os
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings.dev')
        django.setup()
    
    # Run tests
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["__main__"])