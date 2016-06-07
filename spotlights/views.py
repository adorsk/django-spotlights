import copy
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from rest_framework import permissions, viewsets

from .models import Display, Queue, Slide
from .serializers import SlideSerializer

class SlideViewSet(viewsets.ModelViewSet):
    queryset = Slide.objects.all()
    serializer_class = SlideSerializer
    permission_classes = [permissions.AllowAny]

def show_next_slide_for_display(request, display_id):
    display = Display.objects.get(pk=display_id)
    queue = display.queue
    historys = request.session.get('historys', {})
    slide_route = queue.get_next_slide_route(historys=historys)
    if slide_route:
        slide = slide_route['slide']
        slide_path = slide_route['path']
        updated_historys = _get_updated_historys(historys, slide_path)
    else:
        slide = None
        slide_path = None
        updated_historys = historys
    request.session['historys'] = updated_historys
    display_admin_url = request.build_absolute_uri(
        reverse('admin:spotlights_display_change', args=(queue.id,)))
    return render(request, 'spotlights/display_item_view.html', context={
        'slide': slide,
        'slide_path': slide_path,
        'display': display,
        'display_admin_url': display_admin_url,
    })

def _get_updated_historys(historys, slide_path):
    updated_historys = copy.deepcopy(historys)
    path_component_index = 0
    for i in range(len(slide_path) - 1):
        history_key = str(slide_path[i])
        next_value = str(slide_path[i + 1])
        updated_historys.setdefault(history_key, []).append(next_value)
    return updated_historys

def manage_display(request, display_id):
    display = Display.objects.get(pk=display_id)
    return render(request, 'spotlights/display_manage_view.html', context={
        'display': display,
    })
