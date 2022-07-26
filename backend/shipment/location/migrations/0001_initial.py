# Generated by Django 4.0 on 2022-03-18 07:28

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0013_add_aramex_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='name')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.customuser', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Service Provider',
                'verbose_name_plural': 'Service Providers',
            },
        ),
        migrations.CreateModel(
            name='CountryCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('country_code', models.CharField(max_length=2, unique=True, verbose_name='Country code')),
                ('country_name', models.CharField(max_length=128, verbose_name='Country name')),
                ('service_provider', models.ManyToManyField(related_name='countries', to='location.ServiceProvider')),
            ],
            options={
                'verbose_name': 'Country Code',
                'verbose_name_plural': 'Country Codes',
            },
        ),
        migrations.CreateModel(
            name='CityCountryServiceProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('city_name', models.CharField(max_length=128, verbose_name='City name')),
                ('country', models.ForeignKey(on_delete=django.db.models.fields.CharField, related_name='cities', to='location.countrycode')),
                ('service_provider', models.ManyToManyField(related_name='cities', to='location.ServiceProvider')),
            ],
            options={
                'verbose_name': 'City with Country and Service Provider',
                'verbose_name_plural': 'Cities with Countries and Service Providers',
                'unique_together': {('country', 'city_name')},
            },
        ),
    ]
