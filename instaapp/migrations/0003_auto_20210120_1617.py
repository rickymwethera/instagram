# Generated by Django 3.1.5 on 2021-01-20 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instaapp', '0002_image_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='name',
            new_name='user',
        ),
    ]
