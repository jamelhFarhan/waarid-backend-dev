# Generated by Django 4.0 on 2022-04-04 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
        ('checkoutdetails', '0005_alter_invoice_payment_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='payment_transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoices', to='payment.paymenttransaction', verbose_name='Payment Transaction'),
        ),
    ]