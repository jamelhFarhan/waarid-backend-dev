# Generated by Django 4.0 on 2022-02-27 19:11
import os

from django.db import migrations
from django.utils import timezone

# apps
from users.models import CustomUser


def create_aramex_user(apps, schema_editor):

    aramex_user = CustomUser(
        is_active=True,
        is_superuser=True,
        is_staff=True,
        username="aramex",
        last_login=timezone.now(),
        email="aramex@mail.com",
        role=3,
        first_name="ARAMEX",
        last_name="delivery unlimited"
    )
    aramex_user.set_password(os.environ.get("ARAMEX_USER_PASSWORD"))
    aramex_user.save()


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0012_alter_customuser_role"),
    ]

    operations = [
        migrations.RunPython(create_aramex_user)
    ]
