# Generated by Django 2.2.3 on 2020-05-09 05:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0005_auto_20200509_1048'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='email_verify',
            new_name='email',
        ),
    ]
