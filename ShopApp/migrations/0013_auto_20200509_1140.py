# Generated by Django 2.2.3 on 2020-05-09 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0012_auto_20200509_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ShopApp.Profile'),
        ),
    ]
