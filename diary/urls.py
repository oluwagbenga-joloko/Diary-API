from django.conf.urls import url
from .views import EntryList, EntryDetail


urlpatterns = [
    url(r'^$',  EntryList.as_view(), name="entry-list"),
    url(r'^(?P<pk>[0-9]+)/$', EntryDetail.as_view(), name="entry-detail")
]