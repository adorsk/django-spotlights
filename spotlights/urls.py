from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'slides', views.SlideViewSet)


app_name = 'spotlights'
urlpatterns = [
    url(r'^display/(?P<display_id>\d+)/', include([
        url(r'^$', views.show_next_slide_for_display),
        url(r'^manage/$', views.manage_display),
    ])),
    url(r'^api/', include(router.urls)),
]
