# Generated by Django 3.1.1 on 2025-01-16 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_follow'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='user',
            new_name='author',
        ),
    ]
