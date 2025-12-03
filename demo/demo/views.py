from django.shortcuts import render, get_object_or_404
from wagtail.contrib.navigation.models import Menu, MenuItem

def menu_preview(request, slug):
    menu = get_object_or_404(Menu, slug=slug)
    return render(request, 'navigation/menu_preview.html', {
        'menu': menu,
        'menu_slug': slug,
    })

def menu_item_detail(request, menu_slug, item_slug):
    menu = get_object_or_404(Menu, slug=menu_slug)
    menu_item = get_object_or_404(MenuItem, menu=menu, slug=item_slug)
    
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
