# Generated by Django 2.2.3 on 2020-05-17 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0026_frontal_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='street_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
