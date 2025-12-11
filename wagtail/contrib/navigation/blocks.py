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
