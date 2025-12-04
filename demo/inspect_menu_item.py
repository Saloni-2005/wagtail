import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings.dev')
django.setup()

from wagtail.contrib.navigation.models import MenuItem

print("MenuItem fields:")
for field in MenuItem._meta.get_fields():
    print(f"- {field.name} ({field.__class__.__name__})")

print("\nChecking for custom_header and custom_footer:")
if hasattr(MenuItem, 'custom_header'):
    print(f"custom_header exists: {MenuItem._meta.get_field('custom_header').__class__.__name__}")
else:
    print("custom_header does NOT exist")

if hasattr(MenuItem, 'custom_footer'):
    print(f"custom_footer exists: {MenuItem._meta.get_field('custom_footer').__class__.__name__}")
else:
    print("custom_footer does NOT exist")
