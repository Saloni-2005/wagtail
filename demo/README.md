# Wagtail Demo - Custom Navigation Feature

This demo showcases Wagtail's custom navigation system, demonstrating how to create flexible, dynamic menus with predefined page types and custom overrides.

## Navigation Feature Overview

The custom navigation system provides:

- **Predefined Page Types**: Quick setup for common pages (About, Contact, Services, etc.)
- **Custom Links**: Support for both internal pages and external URLs
- **Conditional Visibility**: Show/hide menu items based on user authentication
- **Header/Footer Customization**: Override default menu items with custom links
- **Rich Content**: Add rich text content to menu items
- **Icon Support**: Attach icons to menu items
- **Submenu Support**: Create nested navigation structures

## Demo Setup

### Prerequisites

- Python 3.8+
- Django 4.2+
- Wagtail 5.0+

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

4. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the demo:**
   - Frontend: http://localhost:8000
   - Admin: http://localhost:8000/admin

## Demo Features

### 1. Basic Menu Creation

Navigate to **Snippets → Menus** in the admin to create your first menu:

```python
# Example menu configuration
Menu(
    title="Main Navigation",
    slug="main",
    home_page=HomePage.objects.first()
)
```

### 2. Predefined Page Types

The demo includes these predefined types:
- About
- Contact  
- Services
- Products
- Blog
- FAQ
- Team
- Careers
- Privacy Policy
- Terms of Service

### 3. Template Integration

```django
<!-- Load navigation tags -->
{% load navigation_tags %}

<!-- Get menu items -->
{% get_menu 'main' page request.user.is_authenticated as menu_items %}

<!-- Render navigation -->
<nav class="main-nav">
    <ul>
        {% for item in menu_items %}
            <li>
                <a href="{{ item.url }}"
                   {% if item.open_in_new_tab %}target="_blank"{% endif %}>
                    {% if item.icon %}
                        <img src="{{ item.icon.url }}" alt="" class="nav-icon">
                    {% endif %}
                    {{ item.title }}
                </a>
                {% if item.slug %}
                    <!-- Submenu support -->
                    <span class="submenu-indicator">{{ item.slug }}</span>
                {% endif %}
            </li>
        {% endfor %}
    </ul>
</nav>
```

### 4. Custom Header/Footer Links

Override default menu items with custom destinations:

```python
# In the admin, add custom header links
custom_header = [
    {
        'link_type': 'about',
        'page': custom_about_page,  # Override default About page
        'open_in_new_tab': False
    },
    {
        'link_type': 'contact',
        'url': 'https://external-contact-form.com',
        'open_in_new_tab': True
    }
]
```

### 5. Conditional Visibility

Control menu visibility based on user state:

```python
# Menu item configurations
MenuItem(
    title="Member Dashboard",
    show_when="logged_in"  # Only for authenticated users
)

MenuItem(
    title="Sign Up",
    show_when="not_logged_in"  # Only for anonymous users
)
```

## Demo Scenarios

### Scenario 1: Corporate Website

Create a professional navigation structure:

1. **Main Menu**: Home, About, Services, Contact
2. **Header Links**: Custom About page, External contact form
3. **Footer Links**: Privacy Policy, Terms of Service

### Scenario 2: E-commerce Site

Build a product-focused navigation:

1. **Main Menu**: Products, Blog, FAQ, Contact
2. **User-specific items**: Account (logged in), Sign Up (logged out)
3. **Custom overrides**: Products → External catalog

### Scenario 3: Multi-section Site

Demonstrate complex navigation:

1. **Multiple menus**: Main, Footer, Sidebar
2. **Submenus**: Services with sub-categories
3. **Context-aware URLs**: Different URL patterns per section

## Testing the Demo

### 1. Admin Interface

1. Go to `/admin/snippets/wagtailnavigation/menu/`
2. Create a new menu with various item types
3. Test custom header/footer overrides
4. Preview changes in the frontend

### 2. Frontend Navigation

1. Visit the homepage to see the main navigation
2. Test different user states (logged in/out)
3. Verify custom links and overrides work
4. Check responsive behavior

### 3. URL Generation

Test automatic URL generation:
- Default items: `/<menu-slug>/<item-slug>/`
- Page links: Use the page's actual URL
- External links: Direct to external URLs
- Context-aware: Different patterns in menu contexts

## Customization Examples

### Custom Menu Template

```django
<!-- templates/navigation/custom_menu.html -->
<nav class="custom-navigation" role="navigation">
    {% get_menu 'main' page request.user.is_authenticated as nav_items %}
    
    <div class="nav-brand">
        <a href="/">{{ site.site_name }}</a>
    </div>
    
    <ul class="nav-items">
        {% for item in nav_items %}
            <li class="nav-item {% if item.page == page %}active{% endif %}">
                <a href="{{ item.url }}" 
                   class="nav-link"
                   {% if item.open_in_new_tab %}target="_blank" rel="noopener"{% endif %}>
                    {% if item.icon %}
                        <img src="{{ item.icon.url }}" alt="" class="nav-icon">
                    {% endif %}
                    <span>{{ item.title }}</span>
                </a>
            </li>
        {% endfor %}
    </ul>
</nav>
```

### Custom Context Processor

```python
# demo/context_processors.py
from wagtail.contrib.navigation.models import Menu

def navigation_menus(request):
    """Add navigation menus to template context."""
    try:
        return {
            'main_menu': Menu.objects.get(slug='main'),
            'footer_menu': Menu.objects.get(slug='footer'),
        }
    except Menu.DoesNotExist:
        return {}
```

## Troubleshooting

### Common Issues

1. **Menu not appearing**: Check that the menu slug matches the template tag
2. **URLs not working**: Verify menu and item slugs are URL-friendly
3. **Custom overrides not working**: Ensure link types match exactly
4. **Visibility issues**: Test with different user authentication states

### Debug Commands

```bash
# Inspect menu structure
python inspect_menu_item.py

# Check menu items in shell
python manage.py shell
>>> from wagtail.contrib.navigation.models import Menu
>>> menu = Menu.objects.get(slug='main')
>>> for item in menu.menu_items.all():
...     print(f"{item.title}: {item.link}")
```

## Docker Support

The demo includes Docker configuration for easy deployment:

```bash
# Build and run with Docker
docker build -f Dockerfile.custom -t wagtail-nav-demo .
docker run -p 8000:8000 wagtail-nav-demo
```

## Next Steps

After exploring the demo:

1. **Integrate into your project**: Copy the navigation app to your Wagtail site
2. **Customize templates**: Adapt the navigation templates to your design
3. **Extend functionality**: Add new predefined types or custom fields
4. **Performance optimization**: Consider caching for high-traffic sites

## Resources

- [Wagtail Documentation](https://docs.wagtail.org/)
- [Navigation Template Tags](../wagtail/contrib/navigation/templatetags/)
- [Navigation Models](../wagtail/contrib/navigation/models.py)
- [Migration Files](../wagtail/contrib/navigation/migrations/)

## Contributing

Found an issue or want to improve the demo? Please contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

The custom navigation system demonstrates Wagtail's flexibility in creating content management solutions that adapt to diverse website structures and user needs.