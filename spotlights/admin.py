from django.contrib import admin
from django import forms
from django.forms import widgets

from . import models

class ChannelMembershipInline(admin.TabularInline):
    model = models.ChannelMembership
    extra = 1

class ChannelMembershipDisplayForm(forms.ModelForm):
    class Meta:
        model = models.ChannelMembership
        fields = ('slide',)
        widgets = {
            'slide': widgets.TextInput(attrs={'disabled': True})
        }

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            initial['slide'] = kwargs['instance'].slide.title
        forms.ModelForm.__init__(self, *args, **kwargs)

class ChannelMembershipDisplayInline(admin.TabularInline):
    model = models.ChannelMembership
    extra = 0 
    form = ChannelMembershipDisplayForm


class MixChannelMembershipInline(admin.TabularInline):
    model = models.MixChannelMembership
    extra = 2 

class SlideAdmin(admin.ModelAdmin):
    inlines = (ChannelMembershipInline,)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.last_modified_by = request.user
        obj.save()

class ChannelAdmin(admin.ModelAdmin):
    inlines = (ChannelMembershipDisplayInline,)

class MixChannelAdmin(admin.ModelAdmin):
    inlines = (MixChannelMembershipInline,)

admin.site.register(models.Slide, SlideAdmin)
admin.site.register(models.Channel, ChannelAdmin)
admin.site.register(models.MixChannel, MixChannelAdmin)
