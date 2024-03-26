# Generated by Django 5.0.2 on 2024-02-29 12:05

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_post_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='_content_rendered',
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='reply',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
