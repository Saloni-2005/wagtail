from django.shortcuts import render, get_object_or_404, redirect
from wagtail.contrib.navigation.models import Menu, MenuItem

def menu_preview(request, slug):
    menu = get_object_or_404(Menu, slug=slug)
    
    # If menu has a home_url set (external URL), embed it in an iframe
    if menu.home_url:
        class FakeMenuItem:
            def __init__(self, url, menu):
                self.title = "Home"
                self.content = f'<iframe src="{url}" style="width: 100%; height: 80vh; border: none;" title="External Content"></iframe>'
                self.menu = menu
                self.slug = 'home'
                self.custom_header = None
                self.custom_footer = None
        
        fake_item = FakeMenuItem(menu.home_url, menu)
        return render(request, 'navigation/menu_item_detail.html', {
            'menu': menu,
            'menu_item': fake_item,
            'menu_slug': slug,
        })
    
    # If menu has a home_page set, display that page's content
    if menu.home_page:
        # Create a fake menu_item to display the home page content
        class FakeMenuItem:
            def __init__(self, page, menu):
                self.title = page.title
                self.content = getattr(page, 'body', '') or getattr(page, 'content', '')
                self.menu = menu
                self.slug = 'home'
                self.custom_header = None
                self.custom_footer = None
        
        fake_item = FakeMenuItem(menu.home_page, menu)
        return render(request, 'navigation/menu_item_detail.html', {
            'menu': menu,
            'menu_item': fake_item,
            'menu_slug': slug,
        })
    
    # Otherwise show the menu preview
    return render(request, 'navigation/menu_preview.html', {
        'menu': menu,
        'menu_slug': slug,
    })

def menu_item_detail(request, menu_slug, item_slug):
    menu = get_object_or_404(Menu, slug=menu_slug)
    menu_item = get_object_or_404(MenuItem, menu=menu, slug=item_slug)
    
    # If menu_item has custom_header with external URL, embed it as iframe
    if menu_item.custom_header:
        for block in menu_item.custom_header:
            url = block.value.get('url')
            if url:
                # Create iframe content for the custom URL
                iframe_content = f'<iframe src="{url}" style="width: 100%; height: 80vh; border: none;" title="External Content"></iframe>'
                # Prepend iframe to existing content or replace if no content
                if menu_item.content:
                    menu_item.content = iframe_content + '<br><br>' + menu_item.content
                else:
                    menu_item.content = iframe_content
                break  # Only use the first URL
    
    return render(request, 'navigation/menu_item_detail.html', {
        'menu': menu,
        'menu_item': menu_item,
    })

def menu_item_detail_context(request, context_menu_slug, item_menu_slug, item_slug):
    # Get the context menu (e.g. 'trendo') to use for navigation context
    context_menu = get_object_or_404(Menu, slug=context_menu_slug)
    
    # Get the actual menu item from its origin menu (e.g. 'header')
    item_menu = get_object_or_404(Menu, slug=item_menu_slug)
    menu_item = get_object_or_404(MenuItem, menu=item_menu, slug=item_slug)
    
    # If menu_item has custom_header with external URL, embed it as iframe
    if menu_item.custom_header:
        for block in menu_item.custom_header:
            url = block.value.get('url')
            if url:
                # Create iframe content for the custom URL
                iframe_content = f'<iframe src="{url}" style="width: 100%; height: 80vh; border: none;" title="External Content"></iframe>'
                # Prepend iframe to existing content or replace if no content
                if menu_item.content:
                    menu_item.content = iframe_content + '<br><br>' + menu_item.content
                else:
                    menu_item.content = iframe_content
                break  # Only use the first URL
    
    return render(request, 'navigation/menu_item_detail.html', {
        'menu': context_menu,  # Pass context menu as 'menu' so navigation stays correct
        'menu_item': menu_item,
    })

def login_view(request):
    return render(request, 'login.html')

def profile_view(request):
    return render(request, 'profile.html')

def login_view_context(request, context_menu_slug):
    context_menu = get_object_or_404(Menu, slug=context_menu_slug)
    return render(request, 'login.html', {
        'menu': context_menu,
    })

def profile_view_context(request, context_menu_slug):
    context_menu = get_object_or_404(Menu, slug=context_menu_slug)
    return render(request, 'profile.html', {
        'menu': context_menu,
    })
