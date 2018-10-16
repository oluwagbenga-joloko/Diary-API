from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.mixins import UpdateModelMixin
from .models import Entry
from .serializers import EntrySerializer

# Create your views here.


class EntryList(ListCreateAPIView):

    serializer_class = EntrySerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

class EntryDetail(RetrieveDestroyAPIView, UpdateModelMixin):
    serializer_class = EntrySerializer

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)




