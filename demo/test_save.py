import os
import sys
import django

# Setup Django
sys.path.append("c:\\Users\\chaud\\OneDrive\\Documents\\Desktop\\wagtail")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings.base")
django.setup()

from wagtail.contrib.navigation.models import Menu, MenuItem

# Try to manually save some data to test
print("Testing manual save of custom_header...")

about_item = MenuItem.objects.get(slug='about', menu__slug='header')
print(f"Found: {about_item.title}")
print(f"Current custom_header: {about_item.custom_header}")
print(f"Current custom_header length: {len(about_item.custom_header) if about_item.custom_header else 0}")

# Try to add a link manually
print("\nAttempting to add a custom header link...")
try:
    about_item.custom_header = [
        ('link', {
            'link_type': 'about',
            'title': '',
            'url': 'https://www.wikipedia.org/',
            'page': None,
            'open_in_new_tab': True
        })
    ]
    about_item.save()
    print("Saved successfully!")
    
    # Reload and check
    about_item.refresh_from_db()
    print(f"After save - custom_header length: {len(about_item.custom_header)}")
    print(f"After save - custom_header: {about_item.custom_header}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
