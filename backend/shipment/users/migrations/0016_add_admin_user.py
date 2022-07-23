# Generated by Django 4.0 on 2022-04-13 07:12

from django.db import migrations
from django.contrib.auth import get_user_model
from django.conf import settings


def add_super_user(apps, schema_editor):
    UserModel = get_user_model()
    user = UserModel.objects.create_user(username=settings.DJANGO_ADMIN_USER,
                                         password=settings.DJANGO_ADMIN_PASSWORD)
    # user = UserModel.objects.create_user('admin',
    #                                      'admin')
    user.is_superuser = True
    user.is_admin = True
    user.is_staff = True
    user.is_active = True
    user.save()


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0015_auto_20220412_1049'),
    ]

    operations = [
        migrations.RunPython(add_super_user)
    ]
