# Generated by Django 4.0 on 2022-01-11 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_container_order_package_order_parcel_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='volume',
            field=models.IntegerField(blank=True, null=True, verbose_name='Volume'),
        ),
    ]
