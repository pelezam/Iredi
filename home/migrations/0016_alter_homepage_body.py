# Generated by Django 5.0.9 on 2024-10-03 19:31

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_homepage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField([('slider', 0), ('top_feature', 1), ('about', 10), ('fact', 13), ('feature', 15), ('services', 16), ('blogs', 16), ('testimonials', 17)], blank=True, block_lookup={0: ('home.blocks.CarouselBlock', (), {}), 1: ('home.blocks.TopFeatureBlock', (), {}), 2: ('wagtail.images.blocks.ImageChooserBlock', (), {'required': False}), 3: ('wagtail.blocks.CharBlock', (), {'required': False}), 4: ('wagtail.blocks.CharBlock', (), {}), 5: ('wagtail.blocks.TextBlock', (), {'required': False}), 6: ('wagtail.blocks.PageChooserBlock', (), {'required': False}), 7: ('wagtail.blocks.CharBlock', (), {'help_text': 'exemple: fa fa-award fa-3x', 'required': False}), 8: ('wagtail.blocks.StructBlock', [[('icon', 7), ('title', 3), ('description', 5)]], {}), 9: ('wagtail.blocks.ListBlock', (8,), {'max_num': 2, 'required': False}), 10: ('wagtail.blocks.StructBlock', [[('image', 2), ('title', 3), ('title_caption', 4), ('subtitle', 3), ('description', 5), ('cta_txt', 3), ('cta_url', 6), ('icon_cards', 9)]], {}), 11: ('wagtail.blocks.StructBlock', [[('title', 4), ('subtitle', 3)]], {}), 12: ('wagtail.blocks.ListBlock', (11,), {'max_num': 4}), 13: ('wagtail.blocks.StructBlock', [[('image', 2), ('facts', 12)]], {}), 14: ('wagtail.blocks.ListBlock', (8,), {'max_num': 3, 'required': False}), 15: ('wagtail.blocks.StructBlock', [[('title', 4), ('subtitle', 3), ('description', 5), ('cta_text', 3), ('cta_url', 6), ('icons', 14)]], {}), 16: ('wagtail.blocks.StructBlock', [[('title', 3), ('subtitle', 3)]], {}), 17: ('wagtail.blocks.StructBlock', [[('title', 3), ('subtitle', 3), ('content', 5), ('cta_txt', 3), ('cta_url', 6)]], {})}),
        ),
    ]
