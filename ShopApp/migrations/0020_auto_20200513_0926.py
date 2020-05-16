# Generated by Django 2.2.3 on 2020-05-13 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0019_droplocation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='droplocation',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='drop_location', to='ShopApp.Profile'),
        ),
    ]