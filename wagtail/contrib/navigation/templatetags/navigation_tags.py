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

        # Prepare custom overrides
        custom_overrides = {}
        custom_stream = None
        
        # Determine which custom stream to use based on the requested menu slug (header/footer)
        if slug == 'header':
            custom_stream = menu.custom_header
        elif slug == 'footer':
            custom_stream = menu.custom_footer
            
        if custom_stream:
            for block in custom_stream:
                if block.block_type == 'link':
                    link_type = block.value.get('link_type')
                    if link_type and link_type != 'custom':
                        custom_overrides[link_type] = block.value

        menu_items = []
        
        # First, add all regular menu items that DON'T have custom overrides
        for candidate in candidates:
            if candidate.show(logged_in):
                # Check if this item type has a custom override
                override_data = custom_overrides.get(candidate.item_type)
                
                if not override_data:
                    # No override - use default behavior
                    url = candidate.trans_url()
                    
                    # If we are in a specific menu context, override the links (existing logic)
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
                        'icon': candidate.icon,
                        'open_in_new_tab': candidate.open_in_new_tab
                    })
        
        # Then, add custom header/footer links (these replace any matching menu items)
        if custom_stream:
            for block in custom_stream:
                if block.block_type == 'link':
                    link_data = block.value
                    link_type = link_data.get('link_type')
                    
                    # Determine the URL
                    url = None
                    page = link_data.get('page')
                    external_url = link_data.get('url')
                    
                    if page:
                        url = page.url
                    elif external_url:
                        url = external_url
                    else:
                        # For standard types without explicit URL, generate default URL
                        if current_menu_slug and link_type != 'custom':
                            url = f"/{current_menu_slug}/{link_type}/"
                        else:
                            url = f"/{link_type}/"
                    
                    # Determine the title
                    title = link_data.get('title')
                    if not title:
                        # Use the display label for the link type
                        from ..models import ITEM_TYPE_CHOICES, HEADER_LINK_CHOICES, FOOTER_LINK_CHOICES
                        all_choices = dict(ITEM_TYPE_CHOICES + HEADER_LINK_CHOICES + FOOTER_LINK_CHOICES)
                        title = all_choices.get(link_type, link_type.title())
                    
                    menu_items.append({
                        'title': title,
                        'url': url,
                        'slug': None,  # Custom links don't have submenus
                        'page': page,
                        'icon': None,  # Custom links don't have icons in current implementation
                        'open_in_new_tab': link_data.get('open_in_new_tab', False)
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
