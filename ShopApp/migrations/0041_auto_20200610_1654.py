# Generated by Django 2.2.3 on 2020-06-10 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0040_auto_20200610_1653'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='user',
            new_name='profile',
        ),
    ]