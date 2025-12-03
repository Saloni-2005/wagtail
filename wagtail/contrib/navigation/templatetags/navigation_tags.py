from django import template
from django.utils import translation
from ..models import Menu

register = template.Library()

@register.simple_tag(takes_context=True)
def get_menu(context, slug, page, logged_in):
    # returns a list of dicts with title, url, slug, page and icon of all items in the menu of the given slug or page
    
    # Try to find a custom menu by slug
    try:
        menu = Menu.objects.get(slug=slug)
        candidates = menu.menu_items.all()
        
        menu_items = []
        for candidate in candidates:
            if candidate.show(logged_in):
                menu_items.append({
                    'title': candidate.title,
                    'url': candidate.trans_url(),
                    'slug': candidate.slug_of_submenu,
                    'page': candidate.trans_page(),
                    'icon': candidate.icon
                })
        return menu_items
    except Menu.DoesNotExist:
        pass

    # If no custom menu, try to use page children
    if page:
        try:
            candidates = page.get_children().live().in_menu()
            menu_items = []
            for candidate in candidates:
                menu_items.append({
                    'title': candidate.title,
                    'url': candidate.url,
                    'slug': None,
                    'page': candidate,
                    'icon': None
                })
            return menu_items
        except AttributeError:
            pass
            
    return None
