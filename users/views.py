import functools
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.utils import jwt_encode_handler
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from .permissions import IsOwnerOrReadOnly
from .utils import jwt_payload_handler
from .models import User
from .serializers import UserSerializer, UserLoginSerializer
from google.oauth2 import id_token as google_verify
from google.auth.transport import requests
from django.conf import settings
from django.contrib.auth import authenticate


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

class UserLogin(APIView):
    permission_classes = ()
    authentication_classes = ()

    

    def post(self, request, format=None):
        serializer =  UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = authenticate(**serializer.validated_data)
            print(user)
            if user and user.provider == "default":
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                return Response({"token": token}, status=status.HTTP_201_CREATED)
            else:
                return Response({"nonFieldErrors": ["Unable to log in with provided credentials."]}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)

class TokenAuth(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, format=None):
        if "id_token" not in request.data:
            return Response({"error": "idToken is required"}, status=status.HTTP_400_BAD_REQUEST)

        id_token = request.data["id_token"]
        try: 
            request_with_timeout = functools.partial(requests.Request(), timeout=2)
            id_info = google_verify.verify_oauth2_token(id_token, request_with_timeout , settings.GOOGLE_CLIENT_ID)

            if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            try: 
                user = User.objects.get(email=id_info["email"])
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                return Response({"token": token}, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                data = {
                "first_name": id_info["given_name"],
                "last_name": id_info["family_name"],
                "email": id_info["email"],
                "password": settings.DEFAULT_PASSWORD
                }

                serializer = UserSerializer(data=data)
                if serializer.is_valid():
                    user = serializer.save(provider="google")
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    return Response({"user": serializer.data, "token": token}, status=status.HTTP_201_CREATED)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        except ValueError as e:
            print(e)
            return Response({"error": "invalid idToken"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"error": "an unkown error occured"})





