from django import template
from django.templatetags.static import static
from django.conf import settings

register = template.Library()

@register.simple_tag
def fixed_static(path):
    """
    A more reliable static file resolver that works with manifest storage
    """
    try:
        return static(path)
    except Exception as e:
        # Fallback to basic static URL if there's an issue
        return settings.STATIC_URL + path