"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from dj_rest_auth.views import PasswordResetConfirmView

from .views import CustomRegisterView, CustomLoginView, CustomPasswordResetView


urlpatterns = [
    path('v1/', include('api.v1.urls')),
    # auth urls
    path('dj-rest-auth/login/',
         CustomLoginView.as_view()),
    path('dj-rest-auth/password/reset/',
         CustomPasswordResetView.as_view()),
    path('dj-rest-auth/password/reset/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/',
         CustomRegisterView.as_view()),
    path('dj-rest-auth/registration/',
         include('dj_rest_auth.registration.urls')),
]
