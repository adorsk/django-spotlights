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

admin.site.register(QueueItem)
admin.site.register(Slide)
