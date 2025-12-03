from django.db import models

from wagtail.models import Page


class HomePage(Page):
    pass


class NavigationDemoPage(Page):
    """A page to demonstrate navigation features"""
    
    template = 'home/navigation_demo.html'
    
    class Meta:
        verbose_name = "Navigation Demo Page"
