import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class TimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Queue(TimestampedModel):
    title = models.CharField(max_length=200)

    def __str__(self):
        return "[Q] {}".format(self.title)

    def get_next_queue_item(self, ids_to_exclude=[], all_queues_history={}):
        next_item = None
        filters = {}
        queue_history = all_queues_history.get(str(self.id))
        if queue_history:
            previous_queue_item_id = queue_history[-1]
            if previous_queue_item_id:
                filters['id__gt'] = previous_queue_item_id

        excludes = {}
        if ids_to_exclude: 
            excludes['item_id__in'] = ids_to_exclude

        ordered_items = self.queueitem_set.order_by(
            'id').exclude(**excludes)

        next_queue_item = ordered_items.filter(**filters).first()

        if not next_queue_item:
            if self.queueitem_set.count() > 0:
                next_queue_item = ordered_items.first()

        if next_queue_item:
            if isinstance(next_queue_item.item, Queue):
                next_queue_item = next_queue_item.get_next_queue_item(
                    ids_to_exclude=(ids_to_exclude + [self.id]),
                    all_queues_history=all_queues_history,
                    filters=filters,
                )
        return next_queue_item

class QueueItem(TimestampedModel):
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE)
    item_content_type = models.ForeignKey(ContentType)
    item_id = models.PositiveIntegerField()
    item = GenericForeignKey('item_content_type', 'item_id')

    def __str__(self):
        return "[QI] QueueID:{}; ItemID:{}; ItemType:{}".format(
            self.queue.id,
            self.item_id,
            self.item_content_type,
        )

class Display(TimestampedModel):
    title = models.CharField(max_length=200)
    queue = models.OneToOneField(
        Queue, editable=False, on_delete=models.CASCADE)
                                 
    def __str__(self):
        return "(Display) {}".format(self.title)

class BaseSlide(TimestampedModel):
    title = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(
        User, blank=True, null=True, editable=False,
        related_name='%(class)s_for_author')
    last_modified_by = models.ForeignKey(
        User, blank=True, null=True, editable=False,
        related_name='%(class)s_for_modifier')
    caption = models.CharField(max_length=200, blank=True)

    class Meta(TimestampedModel.Meta):
        abstract = True

    def __str__(self):
        return "({}) {}".format(type(self).__name__, self.title)

def _get_slide_media_path(instance, filename):
    return 'slides/{slide_id}__{filename}__{datetime}'.format(
        slide_id=instance.id,
        filename=filename,
        datetime=datetime.datetime.now().isoformat()
    )

class ImageSlide(BaseSlide):
    image_file = models.FileField(upload_to=_get_slide_media_path, blank=True)

class UrlSlide(BaseSlide):
    url = models.CharField(max_length=1024, blank=True)
