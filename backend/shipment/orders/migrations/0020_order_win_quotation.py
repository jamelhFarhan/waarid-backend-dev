# Generated by Django 4.0 on 2022-02-23 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0019_remove_order_consignee_remove_order_consignor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='win_quotation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booked_order', to='orders.quotation'),
        ),
    ]