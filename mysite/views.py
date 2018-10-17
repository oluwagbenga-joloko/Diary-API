from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse


class RootView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        return Response({
            "entries":  reverse('entry-list', request=request),
            "users": reverse('user-list', request=request)
        })


