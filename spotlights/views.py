from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView

from . import models

class SlideDetail(DetailView):
    model = models.Slide

def channel_index(request, channel_id):
    channel = models.Channel.objects.get(id=channel_id)
    slide = _get_next_slide_for_channel(channel, request)
    _update_prev_slide_for_channel(channel, request, slide)
    return render(request, 'spotlights/channel_index.html', context={
        'slide': slide,
        'channel': channel
    })

def _get_next_slide_for_channel(channel, request):
    slide = None

    prev_slide_key = None
    channel_key = _get_channel_key(channel)
    if ('channels' in request.session and 
        channel_key in request.session['channels']):
        prev_slide_key = request.session['channels'][channel_key].get(
            'prev_slide_key')
    if prev_slide_key:
        prev_slide_id = int(prev_slide_key)
        slide = channel.get_slide_after(prev_slide_id)
    if not slide:
        slide = channel.get_first_slide()
    return slide

def _get_channel_key(channel):
    return str(channel.id)

def _update_prev_slide_for_channel(channel, request, prev_slide):
    channel_key = _get_channel_key(channel)
    prev_slide_key = _get_slide_key(prev_slide)
    if 'channels' not in request.session:
        request.session['channels'] = {}
    if channel_key not in request.session['channels']:
        request.session['channels'][channel_key] = {}
    request.session['channels'][channel_key]['prev_slide_key'] = prev_slide_key
    request.session.modified = True

def _get_slide_key(slide):
    return str(slide.id)

def mixchannel_index(request, mixchannel_id):
    mixchannel = models.MixChannel.objects.get(id=mixchannel_id)
    channel = _get_next_channel_for_mixchannel(mixchannel, request)
    slide = _get_next_slide_for_channel(channel, request)

    _update_prev_slide_for_channel(channel, request, slide)
    _update_prev_channel_for_mixchannel(mixchannel, request, channel)

    slide_channel_titles = [membership.channel.title
                            for membership in slide.channelmembership_set.all()]

    return render(request, 'spotlights/mixchannel_index.html', context={
        'slide': slide,
        'channel': channel,
        'mixchannel': mixchannel,
        'slide_channel_titles': slide_channel_titles,
    })

def _get_next_channel_for_mixchannel(mixchannel, request):
    channel = None
    prev_channel_key = None
    mixchannel_key = _get_mixchannel_key(mixchannel)
    if ('mixchannels' in request.session and 
        mixchannel_key in request.session['mixchannels']):
        prev_channel_key = request.session['mixchannels'][mixchannel_key].get(
            'prev_channel_key')
    if prev_channel_key:
        prev_channel_id = int(prev_channel_key)
        channel = mixchannel.get_channel_after(prev_channel_id)
    if not channel:
        channel = mixchannel.get_first_channel()
    return channel

def _get_mixchannel_key(mixchannel):
    return str(mixchannel.id)

def _update_prev_channel_for_mixchannel(mixchannel, request, prev_channel):
    mixchannel_key = _get_mixchannel_key(mixchannel)
    prev_channel_key = _get_channel_key(prev_channel)
    if 'mixchannels' not in request.session:
        request.session['mixchannels'] = {}
    if mixchannel_key not in request.session['mixchannels']:
        request.session['mixchannels'][mixchannel_key] = {}
    session_shard = request.session['mixchannels'][mixchannel_key]
    session_shard['prev_channel_key'] = prev_channel_key
    request.session.modified = True
