# Generated by Django 2.2.3 on 2020-05-21 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0030_auto_20200518_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='sizes',
        ),
        migrations.DeleteModel(
            name='Sizes',
        ),
    ]