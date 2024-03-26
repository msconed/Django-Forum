# Generated by Django 5.0.2 on 2024-02-28 09:47

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_comment_content_alter_reply_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='reply',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]