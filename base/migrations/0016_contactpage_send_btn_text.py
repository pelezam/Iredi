# Generated by Django 5.0.9 on 2024-10-06 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_contactpage_page_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactpage',
            name='send_btn_text',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
