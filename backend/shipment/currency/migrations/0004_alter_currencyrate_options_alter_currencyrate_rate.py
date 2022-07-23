# Generated by Django 4.0 on 2022-05-27 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0003_auto_20220405_0842'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currencyrate',
            options={'ordering': ['-date'], 'verbose_name': 'Currency Rate', 'verbose_name_plural': 'Currency Rates'},
        ),
        migrations.AlterField(
            model_name='currencyrate',
            name='rate',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Rate'),
        ),
    ]