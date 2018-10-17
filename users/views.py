from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.utils import jwt_encode_handler
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from .permissions import IsOwnerOrReadOnly
from .utils import jwt_payload_handler
from .models import User
from .serializers import UserSerializer

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
    

class UserDetail(RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)
