# Generated by Django 4.0 on 2022-01-21 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_alter_order_options_remove_order_archived_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='description',
            field=models.TextField(default='', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='note',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='orders.request', verbose_name='Request'),
        ),
    ]