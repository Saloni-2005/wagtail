from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from django.core.exceptions import ValidationError

ITEM_TYPE_CHOICES = [
    ('about', _('About')),
    ('contact', _('Contact')),
    ('services', _('Services')),
    ('products', _('Products')),
    ('blog', _('Blog')),
    ('faq', _('FAQ')),
    ('team', _('Team')),
    ('careers', _('Careers')),
    ('privacy', _('Privacy Policy')),
    ('terms', _('Terms of Service')),
    ('custom', _('Custom')),
]

HEADER_LINK_CHOICES = [
    ('about', _('About')),
    ('contact', _('Contact')),
    ('services', _('Services')),
    ('products', _('Products')),
    ('blog', _('Blog')),
    ('custom', _('Custom')),
]

FOOTER_LINK_CHOICES = [
    ('privacy', _('Privacy Policy')),
    ('terms', _('Terms of Service')),
    ('faq', _('FAQ')),
    ('contact', _('Contact')),
    ('custom', _('Custom')),
]

class LinkStructValue(blocks.StructValue):
    @property
    def display_title(self):
        link_type = self.get('link_type')
        if link_type == 'custom':
            title = self.get('title')
            if title:
                return title
            page = self.get('page')
            if page:
                return page.title
            return self.get('url')
        else:
            all_choices = dict(ITEM_TYPE_CHOICES + HEADER_LINK_CHOICES + FOOTER_LINK_CHOICES)
            return all_choices.get(link_type, link_type)


class HeaderLinkBlock(blocks.StructBlock):
    link_type = blocks.ChoiceBlock(choices=HEADER_LINK_CHOICES, default='custom', help_text=_("Select the type of link"))
    title = blocks.CharBlock(required=False, help_text=_("Title (Only used for 'Custom' links)"))
    url = blocks.URLBlock(required=False, help_text=_("External URL"))
    page = blocks.PageChooserBlock(required=False, help_text=_("Internal Page"))
    open_in_new_tab = blocks.BooleanBlock(required=False, help_text=_("Open in new tab"))

    class Meta:
        template = "navigation/blocks/link_block.html"
        value_class = LinkStructValue


class FooterLinkBlock(blocks.StructBlock):
    link_type = blocks.ChoiceBlock(choices=FOOTER_LINK_CHOICES, default='custom', help_text=_("Select the type of link"))
    title = blocks.CharBlock(required=False, help_text=_("Title (Only used for 'Custom' links)"))
    url = blocks.URLBlock(required=False, help_text=_("External URL"))
    page = blocks.PageChooserBlock(required=False, help_text=_("Internal Page"))
    open_in_new_tab = blocks.BooleanBlock(required=False, help_text=_("Open in new tab"))

    class Meta:
        template = "navigation/blocks/link_block.html"
        value_class = LinkStructValue


class UniqueLinkStreamBlock(blocks.StreamBlock):
    def __init__(self, block_types=None, **kwargs):
        super().__init__(block_types, **kwargs)
    
    def clean(self, value, **kwargs):
        cleaned_data = super().clean(value, **kwargs)
        errors = {}
        types_seen = set()
        
        for i, child in enumerate(cleaned_data):
            # child.value is a StructValue, so we access it like a dict or attribute
            link_type = child.value.get('link_type')
            
            if link_type and link_type != 'custom':
                if link_type in types_seen:
                    errors[i] = blocks.StreamBlockValidationError(
                        non_block_errors=blocks.ErrorList([
                            ValidationError(f"The link type '{link_type}' can only be added once.")
                        ])
                    )
                types_seen.add(link_type)
        
        if errors:
            raise blocks.StreamBlockValidationError(block_errors=errors)
        return cleaned_data


from .blocks import HeadingBlock, ImageBlock, CardBlock, ButtonBlock, VideoBlock, GridBlock

@register_snippet
class Menu(ClusterableModel):
    title = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='title', editable=True, help_text="Unique identifier of menu. Will be populated automatically from title of menu. Change only if needed.")
    content = StreamField([
        ('heading', HeadingBlock()),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageBlock()),
        ('card', CardBlock()),
        ('button', ButtonBlock()),
        ('video', VideoBlock()),
        ('grid', GridBlock()),
    ], blank=True, use_json_field=True, help_text=_("Content to display for this menu"))
    
    home_page = models.ForeignKey(
        'wagtailcore.Page', blank=True, null=True, related_name='+', on_delete=models.SET_NULL, help_text=_("Page to display on the menu's home screen")
    )
    home_url = models.CharField(max_length=500, blank=True, null=True, help_text=_("External URL to display on the menu's home screen (overrides Page)"))

    custom_header = StreamField(
        UniqueLinkStreamBlock([('link', HeaderLinkBlock())]),
        blank=True, 
        null=True, 
        use_json_field=True, 
        verbose_name=" ",
        help_text=_("Add links to display in the header for this menu.")
    )
    
    custom_footer = StreamField(
        UniqueLinkStreamBlock([('link', FooterLinkBlock())]),
        blank=True, 
        null=True, 
        use_json_field=True, 
        verbose_name=" ",
        help_text=_("Add links to display in the footer for this menu.")
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('slug'),
            FieldPanel('content'),
            PageChooserPanel('home_page'),
            FieldPanel('home_url'),
        ], heading=_("Menu")),
        InlinePanel('menu_items', label=_("Menu Item"))
    ]

    def __str__(self):
        return self.title

class MenuItem(Orderable):
    ITEM_TYPE_CHOICES = ITEM_TYPE_CHOICES

    menu = ParentalKey('Menu', related_name='menu_items', help_text=_("Menu to which this item belongs"))
    item_type = models.CharField(
        max_length=20,
        choices=ITEM_TYPE_CHOICES,
        default='custom',
        help_text=_("Select a predefined page type or choose 'Custom'")
    )
    title = models.CharField(max_length=50, help_text=_("Title of menu item that will be displayed"))
    slug = AutoSlugField(populate_from='title', editable=True, help_text="URL-friendly version of title")
    content = StreamField([
        ('heading', HeadingBlock()),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageBlock()),
        ('card', CardBlock()),
        ('button', ButtonBlock()),
        ('video', VideoBlock()),
        ('grid', GridBlock()),
    ], blank=True, use_json_field=True, help_text=_("Content to display on this menu item's page"))
    link_url = models.CharField(max_length=500, blank=True, null=True, help_text=_("External URL (LEAVE BLANK to use auto-generated page URL)"))

    link_page = models.ForeignKey(
        'wagtailcore.Page', blank=True, null=True, related_name='+', on_delete=models.CASCADE, help_text=_("Link to existing Wagtail page (LEAVE BLANK to use auto-generated page)"),
    )
    title_of_submenu = models.CharField(
        blank=True, null=True, max_length=50, help_text=_("Title of submenu (LEAVE BLANK if there is no custom submenu)")
    )
    open_in_new_tab = models.BooleanField(default=False, help_text=_("Open link in a new tab"))
    icon = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
    )
    show_when = models.CharField(
        max_length=15,
        choices=[('always', _("Always")), ('logged_in', _("When logged in")), ('not_logged_in', _("When not logged in"))],
        default='always',
    )

    panels = [
        FieldPanel('item_type'),
        FieldPanel('title'),
        FieldPanel('slug'),
        FieldPanel('content'),
        PageChooserPanel('link_page'),
        FieldPanel('open_in_new_tab'),
        FieldPanel('title_of_submenu'),
        FieldPanel('icon'),
        FieldPanel('show_when'),
    ]

    def __str__(self):
        return self.title

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        else:
            # Auto-generated URL: /<menu-slug>/<item-slug>/
            return f"/{self.menu.slug}/{self.slug}/"

    def trans_url(self, language_code=None):
        return self.link

    def trans_page(self, language_code=None):
        return self.link_page

    @property
    def slug_of_submenu(self):
        if self.title_of_submenu:
            return slugify(self.title_of_submenu)
        return None

    def show(self, authenticated):
        return ((self.show_when == 'always')
                or (self.show_when == 'logged_in' and authenticated)
                or (self.show_when == 'not_logged_in' and not authenticated))
