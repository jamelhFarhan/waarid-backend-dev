from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import NoteCreateView

app_name = "orders"

urlpatterns = [
    path("quotation_note/", NoteCreateView.as_view(), name="create_note"),
]
