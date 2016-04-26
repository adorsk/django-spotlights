import copy
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
import json

from .models import Display, Queue
from .forms import SlideTypeForm, ImageSlideForm, UrlSlideForm

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

# This stuff is basically a wizard for slide creation.
# Prolly a cleaner way to do this.
# Django formtools doesn't quite work (I think), because it's hard to
# dynamic steps.

def create_slide(request):
    form = SlideTypeForm()
    return _render_create_slide_step_1(form)

def _render_create_slide_step_1(request, form):
    return render(request,
                  'spotlights/create_slide/select_type.html',
                  context={
                      'form': form,
                  })

def process_create_slide_step_1(request):
    slide_type_form = SlideTypeForm(request.post)
    if not slide_type_form.is_valid():
        return _render_create_slide_step_1(request, slide_type_form)
    slide_type = form.cleaned_data['slide_type']
    details_form_cls = _get_form_cls_for_slide_type(slide_type)
    slide_details_form = details_form_cls()
    return _render_create_slide_step_2(request, slide_details_form)

def _get_form_cls_for_slide_type(slide_type):
    if slide_type == 'ImageSlide':
        form_cls = ImageSlideForm
    elif slide_type == 'UrlSlide':
        form_cls = UrlSlideForm
    return form_cls

def _render_create_slide_step_2(request, slide_details_form)
    return render(request,
                  'spotlights/create_slide/slide_details.html',
                  context={
                      'form': slide_details_form,
                  }
                 )

def process_create_slide_step_2(request, slide_type=None):
    details_form_cls = _get_form_cls_for_slide_type(slide_type)
    slide_details_form = details_form_cls(request.post)
    if not slide_details_form.is_valid():
        return _render_create_slide_step_2(request, slide_details_form)
    slide = slide_details_form.save()
    # Create slide item here?
