# Generated by Django 2.2.3 on 2020-05-08 06:17

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categories', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategories', models.CharField(max_length=200, unique=True)),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategory', to='ShopApp.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.IntegerField(null=True)),
                ('location', models.CharField(blank=True, max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=260)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='product_name')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('discount_amount', models.IntegerField(blank=True, default=0, null=True)),
                ('description', models.TextField()),
                ('product_brand', models.CharField(default='None', max_length=250)),
                ('sizes_available', models.CharField(default='XL L M', max_length=200)),
                ('product_pic', models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d/')),
                ('featured', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(default='rohanjha', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advertisements', to='ShopApp.Category')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advertisements', to='ShopApp.SubCategory')),
            ],
        ),
    ]
