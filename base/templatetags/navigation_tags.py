from django import template
from home.models import HomePage
from wagtail.models import Page


register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    #return Site.find_for_request(context["request"]).root_page
    home_page = HomePage.objects.first()
    #return Page.objects.live().in_menu().filter(depth__gt=2)
    return home_page.get_children().live().in_menu()