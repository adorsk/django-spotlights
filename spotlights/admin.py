from django.contrib import admin
from django import forms
from django.forms import widgets

from .models import Queue, QueueItem, ImageSlide, UrlSlide, Display

admin.site.register(Queue)

class ImageSlideAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.last_modified_by = request.user
        obj.save()
admin.site.register(ImageSlide, ImageSlideAdmin)

admin.site.register(UrlSlide)

admin.site.register(QueueItem)

class DisplayAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            queue_title = "_queue-for-{}".format(obj.title)
            queue = Queue(title=queue_title)
            queue.save()
            obj.queue = queue
        obj.save()
admin.site.register(Display, DisplayAdmin)
