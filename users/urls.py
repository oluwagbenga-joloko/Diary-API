from django.conf.urls import url
from users.views import UserList, UserDetail, TokenAuth, UserLogin


urlpatterns = [
    url(r'^$', UserList.as_view(), name='user-list'),
    url(r'^(?P<pk>[0-9]+)/$', UserDetail.as_view(),name='user-detail'),
    url(r'^login/$',  UserLogin.as_view(), name='user-login'),
    url(r'^tokenauth/$', TokenAuth.as_view(), name='token-auth')
]