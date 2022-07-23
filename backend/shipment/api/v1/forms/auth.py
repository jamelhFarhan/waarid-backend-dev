# from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django import forms

from allauth.account.forms import ResetPasswordForm
from allauth.account.forms import default_token_generator
from allauth.account.adapter import get_adapter
from allauth.account.utils import user_pk_to_url_str

from rest_framework.serializers import ValidationError
# apps
from users.models import CustomUser


class CustomResetPasswordForm(ResetPasswordForm):

    def clean_email(self):
        try:
            ret = super().clean_email()
        except forms.ValidationError:
            raise ValidationError(
                _("The e-mail address is not assigned to any user account")
            )

        return ret

    def save(self, request, **kwargs):
        # current_site = get_current_site(request)
        email = self.cleaned_data['email']
        token_generator = kwargs.get('token_generator', default_token_generator)
        template = kwargs.get("email_template")
        user = CustomUser.objects.get(email=email)
        uid = user_pk_to_url_str(user)
        token = token_generator.make_token(user)
        project_host = settings.PROJECT_HOST
        reset_url = f"{request.scheme}://{project_host}/reset-password/{uid}/{token}"
        context = {
            'user': user,
            'password_reset_url': reset_url,
            'request': request,
            'site_name': 'https://deyarat.com'
        }
        context['username'] = user.username
        get_adapter(request).send_mail(template, email, context)
        return email
