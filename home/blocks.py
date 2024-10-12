from wagtail.blocks import ListBlock
from wagtail.blocks import (
    CharBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    PageChooserBlock,
    TextBlock,
    URLBlock
)
from wagtail.images.blocks import ImageChooserBlock
from base.blocks import IconCard
from base.models import BlogPage, ServicePage, Testimonial


class CarouselImageBlock(StructBlock):
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    cta_txt = CharBlock(required=False)
    cta_url = PageChooserBlock(required=False)


class CarouselBlock(ListBlock):
    def __init__(self, **kwargs):
        super().__init__(CarouselImageBlock(), **kwargs)
    
    class Meta:
        icon="image"
        template="home/blocks/carousel_block.html"


class TopFeatureItemBlock(StructBlock):
    icon = CharBlock(required=False, help_text="exemple: fa fa-times")
    title = CharBlock(required=True)
    description = TextBlock(required=False)


class TopFeatureBlock(ListBlock):
    def __init__(self, **kwargs):
        super().__init__(TopFeatureItemBlock(), **kwargs)
    
    class Meta:
        icon="form"
        template="home/blocks/top_feature_block.html"
        min_num = 1
        max_num = 3


class AboutBlock(StructBlock):
    image = ImageChooserBlock(required=False)
    title = CharBlock(required=False)
    title_caption = CharBlock()
    subtitle = CharBlock(required=False)
    description = TextBlock(required=False)
    cta_txt = CharBlock(required=False)
    cta_url = PageChooserBlock(required=False)
    icon_cards = ListBlock(IconCard(), required=False, max_num=2)

    class Meta:
        icon="bars"
        template="home/blocks/about_block.html"


class FactBlock(StructBlock):
    image = ImageChooserBlock(required=False)
    facts = ListBlock(StructBlock((
        ('title', CharBlock()),
        ('subtitle', CharBlock(required=False))
    )),max_num=4)

    class Meta:
        template = "home/blocks/facts_block.html"
        icon ="list-ol"


class FeatureBlock(StructBlock):
    title = CharBlock()
    subtitle = CharBlock(required=False)
    description = TextBlock(required=False)
    cta_text = CharBlock(required=False)
    cta_url = PageChooserBlock(required=False)
    icons = ListBlock(IconCard(), required=False, max_num=3)

    class Meta:
        icon = "info-circle"
        template="home/blocks/features_block.html"


class ServiceBlock(StructBlock):
    title = CharBlock(required=False)
    subtitle = CharBlock(required=False)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        services = ServicePage.objects.all().live()
        context['services'] = services
        return context

    class Meta:
        template = "home/blocks/service_block.html"
        icon = "clipboard-list"


class BlogBlock(StructBlock):
    title = CharBlock(required=False)
    subtitle = CharBlock(required=False)
    
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        blogs = BlogPage.objects.all().order_by("-first_published_at").live()[:3]
        context['blogs'] = blogs
        return context
    
    class Meta:
        template = "home/blocks/blog_block.html"
        icon = "home"

class TestimonialBlock(StructBlock):
    title = CharBlock(required=False)
    subtitle = CharBlock(required=False)
    content = TextBlock(required=False)
    cta_txt = CharBlock(required=False)
    cta_url = PageChooserBlock(required=False)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        testimonials = Testimonial.objects.all()
        context["testimonials"] = testimonials
        return context

    class Meta:
        template = "home/blocks/testimonial_block.html"
    

class HomePageStreamBlock(StreamBlock):
    slider = CarouselBlock()
    top_feature = TopFeatureBlock()
    about = AboutBlock()
    fact = FactBlock()
    feature = FeatureBlock()
    services = ServiceBlock()
    blogs = BlogBlock()
    testimonials = TestimonialBlock()
    

