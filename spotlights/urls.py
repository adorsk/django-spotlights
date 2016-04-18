from django.conf.urls import url, include

from . import views


app_name = 'spotlights'
urlpatterns = [
    url(r'^display/(?P<display_id>\d+)/', include([
        url(r'^$', views.show_next_slide_for_display),
        url(r'^manage/$', views.manage_display),
    ])),
]
