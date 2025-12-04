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
        for candidate in candidates:
            if candidate.show(logged_in):
                # Check for override
                override_data = custom_overrides.get(candidate.item_type)
                
                if override_data:
                    # Use custom data
                    title = override_data.get('title') or candidate.title # Fallback to default title if not provided in custom? Actually custom title is optional for non-custom types usually, but here we want to use it if present.
                    # Wait, the logic for display_title in models.py suggests:
                    # if link_type == 'custom': use title or page.title or url
                    # else: use display label for the choice.
                    # BUT, the user wants to "replace" the item.
                    # If I use the override, I should probably use the override's title if it's a custom link, 
                    # but for standard links (like 'about'), the user might want to keep the standard name OR rename it.
                    # The HeaderLinkBlock has a 'title' field which is "Only used for 'Custom' links" according to help_text.
                    # However, if the user provides a replacement for 'About', they might want to point it to a different URL.
                    
                    # Let's look at HeaderLinkBlock again.
                    # title = blocks.CharBlock(required=False, help_text=_("Title (Only used for 'Custom' links)"))
                    # So for 'about', title might be empty in the override.
                    
                    # If override is present, we should use its URL/Page.
                    # What about the title?
                    # If the user selected 'About' in the override, they probably want the title 'About'.
                    # Unless they selected 'Custom' type? No, we are matching on link_type.
                    # So if candidate.item_type is 'about', we look for an override with link_type='about'.
                    
                    # Let's calculate the URL from the override
                    url = None
                    page = override_data.get('page')
                    external_url = override_data.get('url')
                    
                    if page:
                        url = page.url
                    elif external_url:
                        url = external_url
                    else:
                        # If no URL provided in override, maybe fallback to default? 
                        # Or is the point of override to PROVIDE the link?
                        # If I have an 'About' item in default menu, it auto-generates /slug/about/.
                        # If I override it, I probably want to point it somewhere else.
                        # If I don't provide a URL in the override, what happens?
                        # The HeaderLinkBlock has url and page as optional.
                        pass

                    # If we still don't have a URL from the override, maybe we should fall back to the candidate's default URL?
                    # But the user said "replace".
                    # Let's assume if they override, they provide the destination.
                    # If not, maybe we keep the default URL? 
                    # "if custom is there else the default menuItem"
                    
                    # Let's try to get the title.
                    # If it's a standard type, we might want to use the standard label, OR the candidate's title.
                    # The candidate (MenuItem) has a title.
                    # The override (Block) has a title (optional).
                    
                    final_title = candidate.title
                    if override_data.get('title'):
                         final_title = override_data.get('title')
                    
                    # If it's a standard type like 'about', and no title provided in override, 
                    # we probably stick with the candidate's title (which is likely 'About').
                    
                    menu_items.append({
                        'title': final_title,
                        'url': url if url else candidate.trans_url(), # Fallback to default URL if override doesn't specify?
                        'slug': candidate.slug_of_submenu, # Submenus might be tricky. Assuming overrides don't handle submenus yet.
                        'page': page if page else candidate.trans_page(),
                        'icon': candidate.icon, # Overrides don't have icons in the block definition I saw
                        'open_in_new_tab': override_data.get('open_in_new_tab', False)
                    })
                    
                else:
                    # Default behavior
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
