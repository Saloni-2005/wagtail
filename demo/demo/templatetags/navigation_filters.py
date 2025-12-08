from django import template

register = template.Library()

@register.filter
def merge_customized(menu_items, custom_items):
    """
    Merge custom items with menu items, replacing items at their original positions.
    
    Args:
        menu_items: List of MenuItem dicts from get_menu
        custom_items: StreamField with custom header/footer items
    
    Returns:
        Merged list with custom items replacing their corresponding default items at the same position
    """
    if not menu_items:
        return menu_items
    
    if not custom_items:
        return menu_items
    
    custom_map = {}
    for block in custom_items:
        link_type = block.value.get('link_type')
        if link_type and link_type != 'custom':
            custom_map[link_type] = block
    
    result = []
    for item in menu_items:
        item_type = item.get('item_type') if isinstance(item, dict) else getattr(item, 'item_type', None)
        
        if item_type in custom_map:
            custom_block = custom_map[item_type]
            result.append({
                'title': custom_block.value.display_title,
                'url': item.get('url'), 
                'open_in_new_tab': False, 
                'is_custom': True,
                'external_url': custom_block.value.get('url') 
            })
            del custom_map[item_type]
        else:
            result.append(item)

    for block in custom_map.values():
        result.append({
            'title': block.value.display_title,
            'url': block.value.get('url'), 
            'open_in_new_tab': block.value.get('open_in_new_tab', False),
            'is_custom': True
        })
    
    return result
