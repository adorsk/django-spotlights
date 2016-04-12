from django.contrib import admin
from django import forms
from django.forms import widgets
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Queue, Slide, QueueItem

class QueueItemInline(admin.TabularInline):
    model = QueueItem
    ct_field = 'item_content_type'
    ct_fk_field = 'item_id'

class QueueAdmin(admin.ModelAdmin):
    inlines = [QueueItemInline,]
admin.site.register(Queue, QueueAdmin)

class SlideAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.last_modified_by = request.user
        obj.save()
admin.site.register(Slide, SlideAdmin)

admin.site.register(QueueItem)
