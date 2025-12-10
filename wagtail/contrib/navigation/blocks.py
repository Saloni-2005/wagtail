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
    
    class Meta:
        template = "navigation/blocks/image_block.html"
        icon = "image"
        label = _("Image")


class CardBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    text = blocks.TextBlock(required=True)
    image = ImageChooserBlock(required=False)
    link_url = blocks.URLBlock(label=_("Link URL"), required=False)
    link_text = blocks.CharBlock(label=_("Link Text"), required=False)

    class Meta:
        template = "navigation/blocks/card_block.html"
        icon = "doc-full"
        label = _("Card")


class ButtonBlock(blocks.StructBlock):
    link_url = blocks.URLBlock(label=_("Button URL"), required=True)
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
