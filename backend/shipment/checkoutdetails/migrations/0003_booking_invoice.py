# Generated by Django 4.0 on 2022-03-30 09:50

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
        ('orders', '0025_alter_order_shipment_destination_and_more'),
        ('checkoutdetails', '0002_deyaratcontactcompany_tax_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='orders.order', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Booking',
                'verbose_name_plural': 'Bookings',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('status', models.IntegerField(default=0, verbose_name='Status')),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='checkoutdetails.booking', verbose_name='Booking')),
                ('payment_transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='payment.paymenttransaction', verbose_name='Booking')),
                ('quotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='orders.quotation', verbose_name='Quotation')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
            },
        ),
    ]
