# Generated by Django 5.0.2 on 2024-03-19 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_alter_author_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='email_is_checked',
            field=models.BooleanField(default=False),
        ),
    ]
