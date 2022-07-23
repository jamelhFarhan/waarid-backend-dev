# Generated by Django 4.0 on 2022-01-21 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_company_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.IntegerField(choices=[(1, 'Customer'), (2, 'Unverified Carrier'), (3, 'Verified Carrier')], db_index=True, default=1, verbose_name='Role'),
        ),
    ]
