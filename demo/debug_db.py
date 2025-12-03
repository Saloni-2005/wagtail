import os
import sys
import django
from django.db import connection

# Setup Django
sys.path.append("c:\\Users\\chaud\\OneDrive\\Documents\\Desktop\\wagtail")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings.base")
django.setup()

from wagtail.models import Page
from home.models import HomePage
from wagtail.contrib.navigation.models import Menu, MenuItem

def inspect_db():
    print("Inspecting DB tables...")
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables:", [t[0] for t in tables if 'navigation' in t[0]])
        
        cursor.execute("PRAGMA table_info(wagtailnavigation_menu);")
        columns = cursor.fetchall()
        print("Menu Columns:", [c[1] for c in columns])

        cursor.execute("PRAGMA table_info(wagtailnavigation_menuitem);")
        columns = cursor.fetchall()
        print("MenuItem Columns:", [c[1] for c in columns])

def inspect_tree():
    print("\nInspecting Page Tree...")
    root = Page.get_first_root_node()
    print(f"Root: {root}")
    home = HomePage.objects.first()
    print(f"Home: {home}")
    if home:
        print(f"Home Parent: {home.get_parent()}")
        print(f"Home Path: {home.path}")
        print(f"Home Depth: {home.depth}")
        
        # Try creating a page
        try:
            print("Attempting to create a test page...")
            from home.models import NavigationDemoPage
            page = NavigationDemoPage(title="Test Page", slug="test-page")
            home.add_child(instance=page)
            print("Test page created successfully.")
        except Exception as e:
            print(f"Failed to create test page: {e}")
            import traceback
            traceback.print_exc()

    print("\nChecking Migrations...")
    with connection.cursor() as cursor:
        cursor.execute("SELECT app, name FROM django_migrations WHERE app='wagtailnavigation';")
        migs = cursor.fetchall()
        print("Applied Migrations:", migs)

    print("\nChecking Menu Items...")
    try:
        menu = Menu.objects.get(name='main-menu')
        print(f"Menu: {menu}")
        items = menu.menu_items.all()
        print(f"Total Items: {items.count()}")
        top_items = menu.menu_items.filter(parent__isnull=True)
        print(f"Top Items: {top_items.count()}")
        for item in top_items:
            print(f" - {item.title} (Children: {item.children.count()})")
    except Menu.DoesNotExist:
        print("Main Menu not found!")

if __name__ == "__main__":
    inspect_db()
    inspect_tree()
