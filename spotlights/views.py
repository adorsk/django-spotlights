from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
import json

from .models import Queue

def show_next_item(request, queue_id):
    queue = Queue.objects.get(pk=queue_id)
    all_queues_history = request.session.get('history', {})
    next_item = queue.get_next_item(all_queues_history=all_queues_history)
    if next_item:
        queue_history = all_queues_history.get(str(queue.id), [])
        queue_history.append(next_item.id)
        all_queues_history[str(queue.id)] = queue_history
    request.session['history'] = all_queues_history
    queue_admin_link = request.build_absolute_uri(
        reverse('admin:spotlights_queue_change', args=(queue_id)))
    return render(request, 'spotlights/queue_item_view.html', context={
        'item': next_item,
        'queue': queue,
        'queue_admin_link': queue_admin_link,
    })
