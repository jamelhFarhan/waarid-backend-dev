# Generated by Django 4.0 on 2022-05-31 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0026_order_item_description_order_need_customs_brokerage_and_more'),
        ('tarif_breakdown', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destinationaddresscharges',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='destinationcharges',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='originaddresscharges',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='origincharges',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='porttoportcharges',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Amount'),
        ),
        migrations.CreateModel(
            name='InsuranceCharges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Fee Name')),
                ('comment', models.CharField(blank=True, max_length=255, null=True, verbose_name='Comment')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Amount')),
                ('quotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='insurance_charges', to='orders.quotation', verbose_name='Quotation')),
            ],
        ),
        migrations.CreateModel(
            name='CustomsBrokerageCharges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Fee Name')),
                ('comment', models.CharField(blank=True, max_length=255, null=True, verbose_name='Comment')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Amount')),
                ('quotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customs_brokerage_charges', to='orders.quotation', verbose_name='Quotation')),
            ],
        ),
    ]