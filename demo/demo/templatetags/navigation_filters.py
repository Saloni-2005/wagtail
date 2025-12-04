from django import template

register = template.Library()

@register.filter
def exclude_customized(menu_items, custom_items):
    """
    Exclude menu items whose item_type matches any link_type in custom_items.
    
    Args:
        menu_items: List of MenuItem objects or dicts from get_menu
        custom_items: StreamField with custom header/footer items
    
    Returns:
        Filtered list of menu items excluding those that have been customized
    """
    if not custom_items:
        return menu_items
    
    # Collect all link_types from custom items
    custom_types = set()
    for block in custom_items:
        link_type = block.value.get('link_type')
        if link_type and link_type != 'custom':
            custom_types.add(link_type)
    
    # Filter out menu items with matching item_type
    filtered_items = []
    for item in menu_items:
        # Handle both dict (from get_menu) and MenuItem objects
        if isinstance(item, dict):
            item_type = item.get('item_type')
        else:
            item_type = getattr(item, 'item_type', None)
        
        if item_type not in custom_types:
            filtered_items.append(item)
    
    return filtered_items
