# Generated by Django 2.2.3 on 2020-06-09 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0033_auto_20200601_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='ShopApp.Profile'),
        ),
    ]