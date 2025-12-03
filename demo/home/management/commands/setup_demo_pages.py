from django.core.management.base import BaseCommand
from wagtail.models import Page
from home.models import HomePage, NavigationDemoPage

class Command(BaseCommand):
    help = 'Setup demo pages for navigation'

    def handle(self, *args, **options):
        home = HomePage.objects.first()
        if not home:
            self.stdout.write(self.style.ERROR('Home page not found'))
            return

        pages = [
            {'title': 'Navigation Demo', 'slug': 'navigation-demo'},
            {'title': 'About', 'slug': 'about', 'children': [
                {'title': 'Our Story', 'slug': 'story'},
                {'title': 'Team', 'slug': 'team'},
            ]},
            {'title': 'Contact', 'slug': 'contact'},
            {'title': 'Services', 'slug': 'services', 'children': [
                {'title': 'Web Development', 'slug': 'web'},
                {'title': 'Consulting', 'slug': 'consulting'},
            ]},
            {'title': 'Privacy Policy', 'slug': 'privacy'},
            {'title': 'Terms of Service', 'slug': 'terms'},
            {'title': 'Support', 'slug': 'support'},
        ]

        for page_data in pages:
            self.create_page(home, page_data)

        self.stdout.write(self.style.SUCCESS('Successfully setup demo pages'))

    def create_page(self, parent, data):
        slug = data['slug']
        title = data['title']
        children = data.get('children', [])

        page = NavigationDemoPage.objects.filter(slug=slug).first()
        if not page:
            page = NavigationDemoPage(title=title, slug=slug)
            parent.add_child(instance=page)
            page.save_revision().publish()
            self.stdout.write(f'Created page: {title}')
        else:
            self.stdout.write(f'Page exists: {title}')

        for child_data in children:
            self.create_page(page, child_data)
