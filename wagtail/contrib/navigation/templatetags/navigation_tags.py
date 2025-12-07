from django import template
from django.utils import translation
from ..models import Menu

register = template.Library()

@register.simple_tag(takes_context=True)
def get_menu(context, slug, page, logged_in):
    try:
        menu = Menu.objects.get(slug=slug)
        candidates = menu.menu_items.all()
        
        current_menu_slug = context.get('menu_slug')
        if not current_menu_slug and context.get('menu'):
            current_menu_slug = context.get('menu').slug

        custom_overrides = {}
        custom_stream = None
        
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
                    
                    url = None
                    page = override_data.get('page')
                    external_url = override_data.get('url')
                    
                    if page:
                        url = page.url
                    elif external_url:
                        url = external_url
                    else:
                        pass
                    
                    final_title = candidate.title
                    if override_data.get('title'):
                         final_title = override_data.get('title')
                    
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
                
                    if current_menu_slug:
                        if candidate.title.lower() == 'home' or candidate.link_url == '/':
                            url = f"/{current_menu_slug}/"
                        elif not candidate.link_url and not candidate.link_page:
                            if candidate.menu.slug == current_menu_slug:
                                url = f"/{current_menu_slug}/{candidate.slug}/"
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
