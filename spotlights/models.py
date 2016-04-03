import datetime
from django.db import models
from django.contrib.auth.models import User

class TimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

def get_slide_image_upload_path(instance, filename):
    return 'slides/{slide_id}__{filename}__{datetime}'.format(
        slide_id=instance.id,
        filename=filename,
        datetime=datetime.datetime.now().isoformat()
    )

class Slide(TimestampedModel):
    title = models.CharField(max_length=200)
    image_file = models.FileField(upload_to=get_slide_image_upload_path, blank=True)
    image_url = models.CharField(max_length=800)
    caption = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(User, related_name='slides', blank=True,
                               null=True, editable=False)
    last_modified_by = models.ForeignKey(User, name='modified_slides',
                                         blank=True, null=True, editable=False)

    def __str__(self):
        return "Slide ({})".format(self.title)

    def get_channels(self):
        return [membership.channel
                for membership in self.channelmembership_set.all()]

class Channel(TimestampedModel):
    title = models.CharField(max_length=200)

    def __str__(self):
        return "Channel ({})".format(self.title)

    def _get_memberships_query(self):
        return self.channelmembership_set.filter(channel=self)

    def _get_ordered_memberships_query(self):
        return self._get_memberships_query().order_by(
            'slide__created')

    def get_first_slide(self):
        slide = None
        membership = self._get_ordered_memberships_query().first()
        if membership:
            slide = membership.slide
        return slide

    def get_slide_after(self, prev_slide_id):
        slide = None
        try:
            prev_slide = Slide.objects.get(id=prev_slide_id)
        except:
            return slide
        later_memberships = self._get_ordered_memberships_query().filter(
            slide__created__gt=prev_slide.created)
        next_membership = later_memberships.first()
        if next_membership:
            slide = next_membership.slide
        return slide

class ChannelMembership(TimestampedModel):
    slide = models.ForeignKey(Slide, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

class MixChannel(TimestampedModel):
    title = models.CharField(max_length=200)

    def __str__(self):
        return "mixChannel ({})".format(self.title)

    def _get_memberships_query(self):
        return self.mixchannelmembership_set.filter(mixchannel=self)

    def _get_ordered_memberships_query(self):
        return self._get_memberships_query().order_by(
            'channel__created')

    def get_first_channel(self):
        channel = None
        membership = self._get_ordered_memberships_query().first()
        if membership:
            channel = membership.channel
        return channel

    def get_channel_after(self, prev_channel_id):
        channel = None
        try:
            prev_channel = Channel.objects.get(id=prev_channel_id)
        except:
            return None
        later_memberships = self._get_ordered_memberships_query().filter(
            channel__created__gt=prev_channel.created)
        next_membership = later_memberships.first()
        if next_membership:
            channel = next_membership.channel
            print("nexto", channel)
        return channel

class MixChannelMembership(TimestampedModel):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    mixchannel = models.ForeignKey(MixChannel, on_delete=models.CASCADE)

