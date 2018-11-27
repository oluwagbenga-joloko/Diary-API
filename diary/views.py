from datetime import datetime
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
        queryset = Entry.objects.filter(user=self.request.user)
        order = self.request.query_params.get('order', None)
        order = self.request.query_params.get('order', None)

        min_created_at = self.request.query_params.get('min_created_at', None)
        max_created_at =  self.request.query_params.get('max_created_at', None)

        if order in ["-created_at", "created_at"]:
            queryset = queryset.order_by(order)

        if min_created_at:
            try:
                print('hererer')
                datetime.strptime(min_created_at,"%Y-%m-%dT%H:%M:%S")
                queryset = queryset.filter(created_at__gte=min_created_at)
            except ValueError:
                pass

        if max_created_at:
            try:
                datetime.strptime(max_created_at, "%Y-%m-%dT%H:%M:%S")
                queryset = queryset.filter(created_at__lte=max_created_at)
            except ValueError:
                pass


        return queryset

class EntryDetail(RetrieveDestroyAPIView, UpdateModelMixin):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = EntrySerializer
    queryset = Entry.objects.all()


    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)




