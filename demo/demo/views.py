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

def login_view(request):
    return render(request, 'login.html')
