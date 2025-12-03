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
        
        # Check for menu_slug or menu in context to override links
        current_menu_slug = context.get('menu_slug')
        if not current_menu_slug and context.get('menu'):
            current_menu_slug = context.get('menu').slug

        menu_items = []
        for candidate in candidates:
            if candidate.show(logged_in):
                url = candidate.trans_url()
                
                # If we are in a specific menu context, override the links
                if current_menu_slug:
                    # Check if it's the Home link (by title or explicit URL)
                    if candidate.title.lower() == 'home' or candidate.link_url == '/':
                        url = f"/{current_menu_slug}/"
                    # For other items, if they are custom (no explicit link)
                    elif not candidate.link_url and not candidate.link_page:
                        # If the item belongs to the current menu, use standard 2-part URL
                        if candidate.menu.slug == current_menu_slug:
                            url = f"/{current_menu_slug}/{candidate.slug}/"
                        # If the item belongs to a different menu (e.g. header/footer), use 3-part URL
                        else:
                            url = f"/{current_menu_slug}/{candidate.menu.slug}/{candidate.slug}/"

                menu_items.append({
                    'title': candidate.title,
                    'url': url,
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
