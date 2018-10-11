from django.shortcuts import render
from django.http import HttpResponseNotFound, Http404
from users.models import User
from users.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from .utils import jwt_payload_handler
from rest_framework_jwt.utils import jwt_encode_handler
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly

# Create your views here.

class UserList(APIView):

    permission_classes = ()
    authentication_classes = ()

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({"user": serializer.data, "token": token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserDetail(APIView):

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise exceptions.NotFound
            
    
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
