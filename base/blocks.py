from wagtail.blocks import CharBlock, TextBlock, StructBlock

class IconCard(StructBlock):
    icon = CharBlock(required=False, help_text="exemple: fa fa-award fa-3x")
    title = CharBlock(required=False)
    description = TextBlock(required=False)
