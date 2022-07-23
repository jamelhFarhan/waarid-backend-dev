from .serializers import ContactUsSerializer
from rest_framework import generics


class ContactUs(generics.ListCreateAPIView):
    serializer_class = ContactUsSerializer

