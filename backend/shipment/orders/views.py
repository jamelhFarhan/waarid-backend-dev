from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Note
from api.v1.serializers.orders import NoteSerializer


class NoteCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
