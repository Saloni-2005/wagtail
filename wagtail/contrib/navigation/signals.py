from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Menu
import json


@receiver(post_save, sender=Menu)
def add_default_custom_links(sender, instance, created, **kwargs):
    """
    Automatically add default custom header/footer links when a new menu is created
    """
    if created and not instance.custom_header and not instance.custom_footer:
        # Add default custom header links
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
        
        # Add default custom footer links
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
        
        try:
            # Only update if the fields are empty
            if not instance.custom_header:
                instance.custom_header = default_header_links
            if not instance.custom_footer:
                instance.custom_footer = default_footer_links
            
            # Save without triggering the signal again
            Menu.objects.filter(pk=instance.pk).update(
                custom_header=instance.custom_header,
                custom_footer=instance.custom_footer
            )
        except Exception:
            # If there's any error, just skip adding defaults
            # This prevents the menu creation from failing
            pass