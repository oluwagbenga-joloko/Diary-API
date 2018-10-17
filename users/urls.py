from django.conf.urls import url
from users.views import UserList, UserDetail
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    url(r'^$', UserList.as_view(), name='user-list'),
    url(r'^(?P<pk>[0-9]+)/$', UserDetail.as_view(),name='user-detail'),
    url(r'^login/$', obtain_jwt_token, name='user-login')
]