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
    
    # Create a mapping of link_type to custom item
    custom_map = {}
    for block in custom_items:
        link_type = block.value.get('link_type')
        if link_type and link_type != 'custom':
            custom_map[link_type] = block
    
    # Build the result list, replacing items where custom versions exist
    result = []
    for item in menu_items:
        item_type = item.get('item_type') if isinstance(item, dict) else getattr(item, 'item_type', None)
        
        # If this item has a custom replacement, use the custom one
        if item_type in custom_map:
            custom_block = custom_map[item_type]
            result.append({
                'title': custom_block.value.display_title,
                'url': item.get('url'),  # Use original item's URL (the page URL, not external URL)
                'open_in_new_tab': False,  # Don't open in new tab since we're embedding
                'is_custom': True,
                'external_url': custom_block.value.url  # Store external URL for reference
            })
            # Remove from map so we don't add it again
            del custom_map[item_type]
        else:
            # Keep the original item
            result.append(item)
    
    # Add any remaining custom items that didn't replace anything
    for block in custom_map.values():
        result.append({
            'title': block.value.display_title,
            'url': block.value.url,  # For new items, use their URL
            'open_in_new_tab': block.value.get('open_in_new_tab', False),
            'is_custom': True
        })
    
    return result
