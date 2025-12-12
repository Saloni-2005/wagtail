from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from django.utils.translation import gettext_lazy as _

class HeadingBlock(blocks.StructBlock):
    text = blocks.CharBlock(label=_("Heading Text"), required=True)
    size = blocks.ChoiceBlock(
        choices=[
            ('h2', 'H2'),
            ('h3', 'H3'),
            ('h4', 'H4'),
        ],
        default='h2',
        label=_("Heading Size")
    )

    class Meta:
        template = "navigation/blocks/heading_block.html"
        icon = "title"
        label = _("Heading")


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    caption = blocks.CharBlock(required=False)
    width = blocks.CharBlock(required=False, default="100%", help_text=_("Width (e.g. 300px, 50%)"))
    height = blocks.CharBlock(required=False, default="auto", help_text=_("Height (e.g. 200px, auto)"))
    
    class Meta:
        template = "navigation/blocks/image_block.html"
        icon = "image"
        label = _("Image")


class CardBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    text = blocks.TextBlock(required=True)
    image = ImageChooserBlock(required=False)
    link_url = blocks.CharBlock(label=_("Link URL"), required=False, help_text=_("URL or relative path (e.g. /about, #, or https://...)"))
    link_text = blocks.CharBlock(label=_("Link Text"), required=False)

    class Meta:
        template = "navigation/blocks/card_block.html"
        icon = "doc-full"
        label = _("Card")


class ButtonBlock(blocks.StructBlock):
    link_url = blocks.CharBlock(label=_("Button URL"), required=True, help_text=_("URL or relative path (e.g. /about, #, or https://...)"))
    text = blocks.CharBlock(label=_("Button Text"), required=True)
    style = blocks.ChoiceBlock(
        choices=[
            ('primary', _('Primary')),
            ('secondary', _('Secondary')),
            ('outline', _('Outline')),
        ],
        default='primary',
        label=_("Button Style")
    )

    class Meta:
        template = "navigation/blocks/button_block.html"
        icon = "placeholder"
        label = _("Button")


class VideoBlock(blocks.StructBlock):
    video = blocks.URLBlock(label=_("Video URL"), help_text=_("YouTube or Vimeo URL"))
    caption = blocks.CharBlock(required=False)
    width = blocks.CharBlock(required=False, default="100%", help_text=_("Width (e.g. 300px, 50%)"))
    height = blocks.CharBlock(required=False, default="auto", help_text=_("Height (e.g. 200px, auto)"))

    class Meta:
        template = "navigation/blocks/video_block.html"
        icon = "media"
        label = _("Video")


class ColumnBlock(blocks.StreamBlock):
    heading = HeadingBlock()
    paragraph = blocks.RichTextBlock()
    image = ImageBlock()
    card = CardBlock()
    button = ButtonBlock()
    video = VideoBlock()

    class Meta:
        template = "navigation/blocks/column_block.html"
        label = _("Column")


class GridBlock(blocks.StructBlock):
    columns = blocks.ChoiceBlock(
        choices=[
            ('2', '2 Columns'),
            ('3', '3 Columns'),
            ('4', '4 Columns'),
        ],
        default='2',
        label=_("Layout")
    )
    content = blocks.StreamBlock([
        ('column', ColumnBlock()),
    ], label=_("Columns"))

    class Meta:
        template = "navigation/blocks/grid_block.html"
        icon = "grip"
        label = _("Grid Layout")


class CarouselItemBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    title = blocks.CharBlock(required=False, max_length=100)
    text = blocks.TextBlock(required=False, max_length=255)
    link_url = blocks.CharBlock(required=False, label=_("Link URL"))
    link_text = blocks.CharBlock(required=False, label=_("Link Text"))

    class Meta:
        label = _("Slide")


class CarouselBlock(blocks.StructBlock):
    items = blocks.ListBlock(CarouselItemBlock(), label=_("Slides"))

    class Meta:
        template = "navigation/blocks/carousel_block.html"
        icon = "image"
        label = _("Hero Carousel")


# Accordion Block
class AccordionItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=100, label=_("Section Title"))
    content = blocks.RichTextBlock(required=True, label=_("Section Content"))
    
    class Meta:
        label = _("Accordion Item")


class AccordionBlock(blocks.StructBlock):
    items = blocks.ListBlock(AccordionItemBlock(), label=_("Accordion Sections"))
    allow_multiple_open = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text=_("Allow multiple sections to be open at once")
    )
    
    class Meta:
        template = "navigation/blocks/accordion_block.html"
        icon = "list-ul"
        label = _("Accordion")


# Tabs Block
class TabItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=50, label=_("Tab Title"))
    content = blocks.RichTextBlock(required=True, label=_("Tab Content"))
    
    class Meta:
        label = _("Tab")


class TabsBlock(blocks.StructBlock):
    tabs = blocks.ListBlock(TabItemBlock(), label=_("Tabs"))
    default_tab = blocks.IntegerBlock(
        required=False,
        default=0,
        help_text=_("Index of the default active tab (0 = first tab)")
    )
    
    class Meta:
        template = "navigation/blocks/tabs_block.html"
        icon = "folder-open-inverse"
        label = _("Tabs")


# Gallery Block
class GalleryImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    caption = blocks.CharBlock(required=False, max_length=200)
    
    class Meta:
        label = _("Gallery Image")


class GalleryBlock(blocks.StructBlock):
    images = blocks.ListBlock(GalleryImageBlock(), label=_("Images"))
    columns = blocks.ChoiceBlock(
        choices=[
            ('2', '2 Columns'),
            ('3', '3 Columns'),
            ('4', '4 Columns'),
        ],
        default='3',
        label=_("Layout")
    )
    enable_lightbox = blocks.BooleanBlock(
        required=False,
        default=True,
        help_text=_("Enable lightbox for full-size image viewing")
    )
    
    class Meta:
        template = "navigation/blocks/gallery_block.html"
        icon = "image"
        label = _("Gallery")


# Timeline Block
class TimelineEventBlock(blocks.StructBlock):
    date = blocks.CharBlock(required=True, max_length=50, label=_("Date"))
    title = blocks.CharBlock(required=True, max_length=100, label=_("Event Title"))
    description = blocks.RichTextBlock(required=True, label=_("Description"))
    image = ImageChooserBlock(required=False, label=_("Event Image"))
    
    class Meta:
        label = _("Timeline Event")


class TimelineBlock(blocks.StructBlock):
    events = blocks.ListBlock(TimelineEventBlock(), label=_("Timeline Events"))
    orientation = blocks.ChoiceBlock(
        choices=[
            ('vertical', _('Vertical')),
            ('horizontal', _('Horizontal')),
        ],
        default='vertical',
        label=_("Orientation")
    )
    
    class Meta:
        template = "navigation/blocks/timeline_block.html"
        icon = "date"
        label = _("Timeline")


# Testimonial Block
class TestimonialItemBlock(blocks.StructBlock):
    name = blocks.CharBlock(required=True, max_length=100, label=_("Name"))
    role = blocks.CharBlock(required=False, max_length=100, label=_("Role/Title"))
    company = blocks.CharBlock(required=False, max_length=100, label=_("Company"))
    text = blocks.TextBlock(required=True, label=_("Testimonial"))
    image = ImageChooserBlock(required=False, label=_("Photo"))
    rating = blocks.IntegerBlock(
        required=False,
        min_value=1,
        max_value=5,
        help_text=_("Rating out of 5 stars")
    )
    
    class Meta:
        label = _("Testimonial")


class TestimonialBlock(blocks.StructBlock):
    testimonials = blocks.ListBlock(TestimonialItemBlock(), label=_("Testimonials"))
    layout = blocks.ChoiceBlock(
        choices=[
            ('single', _('Single')),
            ('grid', _('Grid')),
            ('carousel', _('Carousel')),
        ],
        default='grid',
        label=_("Layout Style")
    )
    
    class Meta:
        template = "navigation/blocks/testimonial_block.html"
        icon = "openquote"
        label = _("Testimonials")

