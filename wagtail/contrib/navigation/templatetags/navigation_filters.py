from django import template

register = template.Library()

@register.filter
def replace(value, args):
    """
    Replaces a string with another string.
    Usage: {{ value|replace:"old|new" }}
    """
    if args and '|' in args:
        old, new = args.split('|')
        return value.replace(old, new)
    return value

@register.filter
def merge_customized(default_items, custom_stream):
    """
    Merges default menu items with customized StreamField overrides.
    """
    if not custom_stream:
        return default_items
    
    custom_items = []
    for block in custom_stream:
        if block.block_type == 'link':
            value = block.value
            custom_items.append({
                'title': value.get('title') or value.get('link_type').title(),
                'url': value.get('url') or (value.get('page').url if value.get('page') else '#'),
                'is_custom': True,
                'open_in_new_tab': value.get('open_in_new_tab'),
            })
            
    if custom_items:
        return custom_items
        
    return default_items
