from django.conf.urls import url

from . import views


app_name = 'spotlights'
urlpatterns = [
    url(r'^queue/(?P<queue_id>\d+)/next_item/$', views.show_next_item),
]
