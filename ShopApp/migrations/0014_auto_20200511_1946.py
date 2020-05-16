# Generated by Django 2.2.3 on 2020-05-11 14:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0013_auto_20200509_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sizes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=120)),
                ('order_size', models.CharField(max_length=20)),
                ('order_quantity', models.IntegerField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('success', models.BooleanField(default=False)),
                ('transact_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopApp.Profile')),
            ],
            options={
                'ordering': ['-transact_date'],
            },
        ),
        migrations.AddField(
            model_name='ad',
            name='sizes',
            field=models.ManyToManyField(to='ShopApp.Sizes'),
        ),
    ]