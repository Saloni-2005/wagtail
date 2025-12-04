import os
import sys
import django

# Setup Django
sys.path.append("c:\\Users\\chaud\\OneDrive\\Documents\\Desktop\\wagtail")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings.base")
django.setup()

from wagtail.contrib.navigation.models import MenuItem

# Check Contact menu item
try:
    contact_item = MenuItem.objects.get(slug='contact', menu__slug='header')
    print(f"Found Contact menu item: {contact_item.title}")
    print(f"Item type: {contact_item.item_type}")
    print(f"\nCustom header exists: {bool(contact_item.custom_header)}")
    
    if contact_item.custom_header:
        print(f"Custom header length: {len(contact_item.custom_header)}")
        print("\nCustom header blocks:")
        for i, block in enumerate(contact_item.custom_header):
            print(f"\n  Block {i}:")
            print(f"    Block type: {block.block_type}")
            print(f"    Link type: {block.value.get('link_type')}")
            print(f"    Title: {block.value.get('title')}")
            print(f"    URL: {block.value.get('url')}")
            print(f"    Page: {block.value.get('page')}")
            print(f"    Open in new tab: {block.value.get('open_in_new_tab')}")
            print(f"    Display title: {block.value.display_title}")
    else:
        print("No custom header configured!")
        
except MenuItem.DoesNotExist:
    print("Contact menu item not found!")
