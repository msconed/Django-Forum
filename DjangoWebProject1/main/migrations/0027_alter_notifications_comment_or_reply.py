# Generated by Django 5.0.2 on 2024-03-17 21:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_notifications_author_notifications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='comment_or_reply',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='main.comment'),
        ),
    ]
