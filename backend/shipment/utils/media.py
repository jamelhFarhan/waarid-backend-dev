import os
import uuid

# from django.conf import settings


def avatar_path(self, filename):
    f_name, f_ext = os.path.splitext(filename)
    return 'avatars/{f_name}'.format(f_name=str(uuid.uuid4()) + f_ext)


def logo_path(self, filename):
    f_name, f_ext = os.path.splitext(filename)
    return 'logo/{f_name}'.format(f_name=str(uuid.uuid4()) + f_ext)


def file_path(self, filename):
    f_name, f_ext = os.path.splitext(filename)
    return 'rates_files/{f_name}'.format(f_name=str(uuid.uuid4()) + f_ext)
