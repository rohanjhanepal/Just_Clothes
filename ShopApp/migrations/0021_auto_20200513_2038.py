# Generated by Django 2.2.3 on 2020-05-13 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0020_auto_20200513_0926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactions',
            name='order_id',
        ),
        migrations.AddField(
            model_name='transactions',
            name='ordered',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ShopApp.Order'),
        ),
    ]