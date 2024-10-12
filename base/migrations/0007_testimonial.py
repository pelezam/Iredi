# Generated by Django 5.0.9 on 2024-10-03 19:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_bloghomepage_blogpage_blogpagetag_blogpage_tags'),
        ('wagtailimages', '0026_delete_uploadedimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(blank=True, max_length=255)),
                ('client_profession', models.CharField(blank=True, max_length=255)),
                ('content', models.TextField(blank=True)),
                ('client_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.image')),
            ],
        ),
    ]
