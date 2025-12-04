from django.test import TestCase
from wagtail.contrib.navigation.models import LinkStructValue
from wagtail.models import Page

class LinkStructValueTest(TestCase):
    def test_url_property_external_url(self):
        block_value = LinkStructValue(None, [('url', 'https://example.com'), ('link_type', 'custom')])
        self.assertEqual(block_value.url, 'https://example.com')

    def test_url_property_internal_page(self):
        root = Page.get_first_root_node()
        page = Page(title="Test Page", slug="test-page")
        root.add_child(instance=page)
        
        block_value = LinkStructValue(None, [('page', page), ('link_type', 'custom')])
        self.assertEqual(block_value.url, page.url)

    def test_url_property_fallback(self):
        block_value = LinkStructValue(None, [('link_type', 'custom')])
        self.assertEqual(block_value.url, '#')
