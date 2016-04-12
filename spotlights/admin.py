from django.contrib import admin
from django import forms
from django.forms import widgets
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Queue, QueueItem, ImageSlide, UrlSlide, Display

class QueueItemInline(admin.TabularInline):
    model = QueueItem
    ct_field = 'item_content_type'
    ct_fk_field = 'item_id'

class QueueAdmin(admin.ModelAdmin):
    inlines = [QueueItemInline,]
admin.site.register(Queue, QueueAdmin)

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
            obj.queue = Queue(title="__{}-queue".format(
                form.cleaned_data['title'])).save()
        obj.save()
admin.site.register(Display, DisplayAdmin)
