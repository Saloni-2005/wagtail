import os
import sys
import django

# Setup Django
sys.path.append("c:\\Users\\chaud\\OneDrive\\Documents\\Desktop\\wagtail")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings.base")
django.setup()

from wagtail.contrib.navigation.models import Menu, MenuItem
import json

# Find the "about" menu item
print("Looking for 'about' menu item...")
about_items = MenuItem.objects.filter(slug='about')
print(f"Found {about_items.count()} items with slug 'about'")

for item in about_items:
    print(f"\n--- Menu Item: {item.title} ---")
    print(f"Menu: {item.menu.title} (slug: {item.menu.slug})")
    print(f"Slug: {item.slug}")
    print(f"Item Type: {item.item_type}")
    
    # Check custom_header
    print(f"\nCustom Header Field:")
    print(f"  Type: {type(item.custom_header)}")
    print(f"  Value: {item.custom_header}")
    
    if item.custom_header:
        print(f"  Length: {len(item.custom_header)}")
        print(f"  Raw JSON: {item.custom_header.raw_data if hasattr(item.custom_header, 'raw_data') else 'N/A'}")
        
        # Try to iterate
        print(f"  Blocks:")
        for i, block in enumerate(item.custom_header):
            print(f"    Block {i}: {block}")
            print(f"      Block Type: {block.block_type}")
            print(f"      Block Value: {block.value}")
            if hasattr(block.value, 'get'):
                print(f"        link_type: {block.value.get('link_type')}")
                print(f"        title: {block.value.get('title')}")
                print(f"        url: {block.value.get('url')}")
                print(f"        page: {block.value.get('page')}")
                print(f"        display_title: {block.value.display_title if hasattr(block.value, 'display_title') else 'N/A'}")
    else:
        print("  Custom header is empty/None")

# Also check all menu items in the "header" menu
print("\n\n=== All items in 'header' menu ===")
try:
    header_menu = Menu.objects.get(slug='header')
    print(f"Header Menu: {header_menu.title}")
    for item in header_menu.menu_items.all():
        print(f"  - {item.title} (slug: {item.slug}, custom_header length: {len(item.custom_header) if item.custom_header else 0})")
except Menu.DoesNotExist:
    print("Header menu not found")
