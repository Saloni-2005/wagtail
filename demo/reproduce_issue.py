import os
import django
from django.conf import settings

# Configure minimal Django settings
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'wagtail.core',
            'wagtail.contrib.navigation',
        ],
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    )
    django.setup()

from wagtail import blocks
from wagtail.contrib.navigation.models import UniqueLinkStreamBlock, HeaderLinkBlock

def test_unique_link_stream_block():
    # Create a block instance
    block = UniqueLinkStreamBlock([('link', HeaderLinkBlock())])
    
    # Mock data that mimics what Wagtail passes to clean()
    # StreamBlock.clean() expects a list of dicts or similar structure representing the stream data
    # But here we can simulate the result of super().clean() if we could.
    # Instead, let's just call clean() with raw data and see what happens.
    
    # Raw data for a StreamBlock is a list of dicts with 'type' and 'value'
    value_data = [
        {
            'type': 'link',
            'value': {
                'link_type': 'contact',
                'title': 'Contact Us',
                'url': 'http://example.com'
            }
        }
    ]
    
    try:
        print("Attempting to clean data...")
        cleaned_data = block.clean(value_data)
        print("Clean successful!")
        
        # Iterate to trigger the loop in clean() if it returns a lazy StreamValue
        # But wait, clean() in UniqueLinkStreamBlock iterates internally!
        # So just calling clean() should trigger the error.
        
    except AttributeError as e:
        print(f"Caught expected error: {e}")
    except Exception as e:
        print(f"Caught unexpected error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_unique_link_stream_block()
