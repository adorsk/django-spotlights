from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^slide/(?P<pk>\d+)/$', views.SlideDetail.as_view()),
    url(r'^channel/(?P<channel_id>\d+)/$', views.channel_index),
    url(r'^mixchannel/(?P<mixchannel_id>\d+)/$', views.mixchannel_index),
]