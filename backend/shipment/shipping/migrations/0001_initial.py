# Generated by Django 4.0 on 2022-04-14 11:53

from django.db import migrations, models
import django.db.models.deletion
import shipping.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0025_alter_order_shipment_destination_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('status', models.IntegerField(choices=[(1, 'IN_PROGRESS'), (2, 'SHIPPED'), (3, 'DELIVERED')], default=shipping.utils.StatusChoice['IN_PROGRESS'], verbose_name='Status')),
                ('tracking_number', models.CharField(max_length=20, verbose_name='Tracking number')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shippings', to='orders.order', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Shipping',
                'verbose_name_plural': 'Shippings',
            },
        ),
        migrations.CreateModel(
            name='ImageShippings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('file', models.FileField(max_length=300, upload_to='shipping_image/%Y/%m/%d/')),
                ('type_code', models.CharField(max_length=20, verbose_name='Type')),
                ('shipping', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shipping.shipping')),
            ],
            options={
                'verbose_name': 'Shipping Image',
                'verbose_name_plural': 'Shipping Images',
            },
        ),
    ]
