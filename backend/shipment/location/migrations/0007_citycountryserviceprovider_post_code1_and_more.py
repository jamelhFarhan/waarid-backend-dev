# Generated by Django 4.0 on 2022-03-25 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0006_citycountryserviceprovider_active_countrycode_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='citycountryserviceprovider',
            name='post_code1',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Post Code1'),
        ),
        migrations.AddField(
            model_name='citycountryserviceprovider',
            name='post_code2',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Post Code2'),
        ),
    ]
