# Generated by Django 2.2.3 on 2020-05-09 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0010_auto_20200509_1109'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='verify',
            new_name='verify_email',
        ),
    ]