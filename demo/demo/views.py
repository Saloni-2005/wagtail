from django.shortcuts import render, get_object_or_404, redirect
from wagtail.contrib.navigation.models import Menu, MenuItem

def menu_preview(request, slug):
    menu = get_object_or_404(Menu, slug=slug)
    
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
    
    if menu.home_page:
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

    url_to_embed = None
    
    if menu.custom_header:
        for block in menu.custom_header:
            url = block.value.get('url')
            if url:
                url_to_embed = url
                break 
    
    if url_to_embed:
        iframe_content = f'<iframe src="{url_to_embed}" style="width: 100%; height: 80vh; border: none;" title="External Content"></iframe>'
        menu_item.content = iframe_content
    
    return render(request, 'navigation/menu_item_detail.html', {
        'menu': menu,
        'menu_item': menu_item,
    })

def menu_item_detail_context(request, context_menu_slug, item_menu_slug, item_slug):
    context_menu = get_object_or_404(Menu, slug=context_menu_slug)

    item_menu = get_object_or_404(Menu, slug=item_menu_slug)
    menu_item = get_object_or_404(MenuItem, menu=item_menu, slug=item_slug)

    url_to_embed = None

    if context_menu.custom_header:
        for block in context_menu.custom_header:
            url = block.value.get('url')
            if url:
                url_to_embed = url
                break  

    if url_to_embed:
        iframe_content = f'<iframe src="{url_to_embed}" style="width: 100%; height: 80vh; border: none;" title="External Content"></iframe>'
        menu_item.content = iframe_content
    
    return render(request, 'navigation/menu_item_detail.html', {
        'menu': context_menu,  
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
