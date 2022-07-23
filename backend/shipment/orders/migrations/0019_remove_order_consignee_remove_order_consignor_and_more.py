# Generated by Django 4.0 on 2022-02-22 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkoutdetails', '0001_initial'),
        ('orders', '0018_alter_quotation_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='consignee',
        ),
        migrations.RemoveField(
            model_name='order',
            name='consignor',
        ),
        migrations.RemoveField(
            model_name='order',
            name='deliveryman',
        ),
        migrations.AddField(
            model_name='order',
            name='consignee_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consignee_orders', to='checkoutdetails.deyaratcontact'),
        ),
        migrations.AddField(
            model_name='order',
            name='consignor_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consignor_orders', to='checkoutdetails.deyaratcontact'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_orders', to='checkoutdetails.deyaratcontact'),
        ),
    ]