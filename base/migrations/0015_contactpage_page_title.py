# Generated by Django 5.0.9 on 2024-10-05 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_contactpage_formfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactpage',
            name='page_title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
