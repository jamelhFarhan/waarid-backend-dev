# Generated by Django 4.0 on 2022-01-07 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_address_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='website',
            field=models.CharField(default='', max_length=30, verbose_name='Website'),
        ),
    ]
