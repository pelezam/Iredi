# Generated by Django 5.0.9 on 2024-10-08 21:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_servicepage_other_service_header'),
        ('wagtailcore', '0094_alter_page_locale'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogTagIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
