# Generated by Django 2.2.3 on 2020-05-13 03:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0018_auto_20200512_1316'),
    ]

    operations = [
        migrations.CreateModel(
            name='DropLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('street_address', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drop_location', to='ShopApp.Profile')),
            ],
        ),
    ]