from django.conf.urls import url
from users.views import UserList, UserDetail
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    url(r'^users/$', UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
    url(r'^/users/login/', obtain_jwt_token),
]