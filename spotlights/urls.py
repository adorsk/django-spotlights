from django.conf.urls import url

from . import views


app_name = 'spotlights'
urlpatterns = [
    url(r'^display/(?P<display_id>\d+)/$', views.show_next_item_for_display),
]
