# Generated by Django 2.2.3 on 2020-05-17 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0027_auto_20200517_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='street_address',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
