from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated

from .models import Entry
from .serializers import EntrySerializer
from .permissions import IsOwnerOrReadOnly

# Create your views here.


class EntryList(ListCreateAPIView):

    serializer_class = EntrySerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

class EntryDetail(RetrieveDestroyAPIView, UpdateModelMixin):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = EntrySerializer
    queryset = Entry.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)




