from django.db import models
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, FieldRowPanel
from wagtail.snippets.models import register_snippet
from django import forms
from wagtail.images import get_image_model
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from modelcluster.models import ClusterableModel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from taggit.models import Tag
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils import timezone
from wagtailcaptcha.models import WagtailCaptchaEmailForm


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


@register_snippet
class SocialNetwork(models.Model):
    name = models.CharField(max_length=250, blank=True)
    icon = models.CharField(max_length=255, blank=True, help_text='"exemple: fab fa-twitter"')
    url = models.URLField(blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("icon"),
        FieldPanel("url")
    ]

    def __str__(self):
        return self.name


@register_setting
class NavigationSettings(BaseGenericSetting):
    topbar = models.BooleanField(default=True)
    logo = models.ForeignKey(get_image_model(), on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    phone = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    socials = models.ManyToManyField(
        "SocialNetwork",
        through="SiteSocialNetwork",
        through_fields=("ns", "sc"),
        verbose_name="Réseaux sociaux")
    banner = models.ForeignKey(get_image_model(), on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    ft_one_title = models.CharField(max_length=250, blank=True)
    ft_one_adress = models.CharField(max_length=255, blank=True)
    ft_two_menu = models.ForeignKey("Menu", on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    ft_three_menu = models.ForeignKey("Menu", on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    ft_four_title = models.CharField(max_length=250, blank=True)
    ft_four_content = RichTextField(blank=True)

    panels = [
        FieldPanel("topbar"),
        FieldPanel("logo"),
        FieldPanel("phone"),
        FieldPanel("email"),
        FieldPanel("banner"),
        FieldPanel('socials', forms.CheckboxSelectMultiple),
        MultiFieldPanel([
            FieldPanel("ft_one_title"),
            FieldPanel("ft_one_adress"),
            FieldPanel("ft_two_menu"),
            FieldPanel("ft_three_menu"),
            FieldPanel("ft_four_title"),
            FieldPanel("ft_four_content"),
        ], heading="footer blocks")
    ]


class SiteSocialNetwork(models.Model):
    sc = models.ForeignKey(SocialNetwork, on_delete=models.CASCADE)
    ns = models.ForeignKey(NavigationSettings, on_delete=models.CASCADE)


class ServiceHomePage(Page):
    template = "base/service_home_page.html"
    max_count = 1
    parent_page_types = ['home.HomePage']

    subtitle = models.CharField(max_length=255, blank=True)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        services = ServicePage.objects.all().live()
        context['services'] = services
        return context



    content_panels = Page.content_panels + [
        FieldPanel('subtitle')
    ]


class ServicePage(Page):
    template = "base/service_page.html"
    parent_page_types = ['base.ServiceHomePage']

    service_image = models.ForeignKey(get_image_model(), on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    subtitle = models.CharField(max_length=255, blank=True)
    service_icon = models.CharField(max_length=255, blank=True)
    content = RichTextField(blank=True)
    cta_txt = models.CharField(max_length=255, blank=True)
    other_service_header = models.CharField(max_length=250, blank=True)


    content_panels = Page.content_panels + [
        FieldPanel("service_image"),
        FieldPanel("subtitle"),
        FieldPanel("service_icon"),
        FieldPanel("content"),
        FieldPanel("cta_txt"),
        FieldPanel("other_service_header")
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        services = ServicePage.objects.exclude(id=self.id).live()
        context['services'] = services
        return context

class BlogHomePage(Page):
    template="base/blog_home_page.html"
    max_count = 1
    parent_page_types = ["home.HomePage"]

    subtitle = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle")
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        blogpages = BlogPage.objects.all().live().public().order_by('-first_published_at')
        page = request.GET.get('page')
        paginator = Paginator(blogpages, 9)
        try:
            blogpages = paginator.page(page)
        except PageNotAnInteger:
            blogpages = paginator.page(1)
        except EmptyPage:
            blogpages = paginator.page(paginator.num_pages)
        context['blogpages'] = blogpages
        return context


class BlogPage(Page):
    template = "base/blog_page.html"
    parent_page_types = ["base.BlogHomePage"]

    intro = models.CharField(max_length=255, blank=True)
    image = models.ForeignKey(get_image_model(), on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    content = RichTextField(blank=True)
    tag_section_title = models.CharField(max_length=250, blank=True)
    other_blog_title = models.CharField(max_length=250, blank=True)


    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("tags"),
        FieldPanel("image"),
        FieldPanel("content"),
        FieldPanel("tag_section_title"),
        FieldPanel("other_blog_title"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        blogpages = BlogPage.objects.exclude(id=self.id).live()
        tags = Tag.objects.all()
        context['blogpages'] = blogpages
        context['tags'] = tags
        return context


@register_snippet
class Testimonial(models.Model):
    client_name = models.CharField(max_length=255, blank=True)
    client_profession = models.CharField(max_length=255, blank=True)
    client_image = models.ForeignKey(get_image_model(), on_delete=models.SET_NULL, blank=True, null=True)
    content = models.TextField(blank=True)


    panels = [
        FieldPanel("client_name"),
        FieldPanel("client_profession"),
        FieldPanel("client_image"),
        FieldPanel("content")
    ]

    def __str__(self):
        return self.client_name


@register_snippet
class Team(models.Model):
    last_name = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    photo = models.ForeignKey(get_image_model(), on_delete=models.SET_NULL, blank=True, null=True)
    profession = models.CharField(max_length=255, blank=True)
    resume = models.TextField(blank=True)

    panels = [
        FieldPanel("last_name"),
        FieldPanel("first_name"),
        FieldPanel("photo"),
        FieldPanel("profession"),
        FieldPanel("resume"),
    ]

    def __str__(self):
        return self.last_name


class AboutPage(Page):
    template = "base/about_page.html"
    max_count = 1
    parent_page_types = ["home.HomePage"]

    subtitle = models.CharField(max_length=255, blank=True)
    image = models.ForeignKey(get_image_model(), on_delete=models.SET_NULL, blank=True, null=True)
    content = RichTextField(blank=True)
    cta_txt = models.CharField(max_length=255, blank=True)
    cta_url = models.ForeignKey("wagtailcore.Page", on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    team_title = models.CharField(max_length=255, blank=True)
    team_subtitle = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("image"),
        FieldPanel("content"),
        FieldPanel("cta_txt"),
        FieldPanel("cta_url"),
        MultiFieldPanel([
         FieldPanel("team_title"),
         FieldPanel("team_subtitle"),  
        ], heading="Team")
    ]


    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        teams = Team.objects.all()
        context['teams'] = teams
        return context


class MenuItem(Orderable):
    link_title = models.CharField(max_length=250, blank=True)
    link_url = models.ForeignKey("wagtailcore.Page", on_delete=models.CASCADE, blank=True, null=True, related_name="+")
    page = ParentalKey("Menu", related_name="menu_items")


@register_snippet
class Menu(ClusterableModel):
    title = models.CharField(max_length=250, blank=True)

    panels = [
        FieldPanel("title"),
        InlinePanel("menu_items", label="Menu Item")
    ]

    def __str__(self):
        return self.title
    


class FormField(AbstractFormField):
    page = ParentalKey('ContactPage', on_delete=models.CASCADE, related_name="form_fields")


class ContactPage(WagtailCaptchaEmailForm):
    template = "base/contact_page.html"
    max_count = 1
    parent_page_types = ["home.HomePage"]

    page_title = models.CharField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    content = RichTextField(blank=True)
    map = models.TextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    send_btn_text = models.CharField(max_length=250, blank=True)


    content_panels = WagtailCaptchaEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel("page_title"),
        FieldPanel("subtitle"),
        FieldPanel("content"),
        FieldPanel("map"),
        FieldPanel("send_btn_text"),
        FieldPanel("thank_you_text"),
        InlinePanel("form_fields", label="form Fields"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel("from_address", classname="col6"),
                FieldPanel("to_address", classname="col6")
            ]),
             FieldPanel("subject")
        ], "Email")
       
    ]


class BlogTagIndexPage(Page):
    template = "base/blog_tag_index_page.html"
    max_count = 1


    def get_context(self, request, *args, **kwargs):
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)
        context  = super().get_context(request, *args, **kwargs)
        context["blogpages"] = blogpages
        return context



class JobPage(Page):
    template = "base/job_page.html"
    parent_page_types = ['base.JobHomePage']

    job_title = models.CharField(max_length=250, blank=True)
    job_description = RichTextField(blank=True)
    status = models.BooleanField(blank=True, default=True)
    publication_date = models.DateTimeField(default=timezone.now)

    content_panels = Page.content_panels + [
        FieldPanel("job_title"),
        FieldPanel("job_description"),
        FieldPanel("status"),
        FieldPanel("publication_date"),
    ]


class JobHomePage(Page):
    template = "base/job_home_page.html"
    max_count = 1
    parent_page_types = ["home.HomePage"]

    subtitle = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        jobs = JobPage.objects.all().live().public()
        context['jobs'] = jobs
        return context


