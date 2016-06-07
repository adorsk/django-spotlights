import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType


class TimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Item(TimestampedModel):
    def __str__(self):
        return "(Item) id:{}".format(self.id)

class QueueItem(TimestampedModel):
    queue = models.ForeignKey('Queue', on_delete=models.CASCADE,
                             related_name='queue')
    item = models.ForeignKey('Item', on_delete=models.CASCADE,
                             related_name='item')


class Queue(Item):
    title = models.CharField(max_length=200)
    items = models.ManyToManyField(Item, through='QueueItem',
                                   related_name='items')

    def __str__(self):
        return "[Q] {}".format(self.title)

    def get_next_slide_route(self, ids_to_exclude=[], historys={}, path=[]):
        slide_route = None
        updated_ids_to_exclude = ids_to_exclude + [self.id]
        updated_path = path + [self.id]

        filters = {}
        queue_history = historys.get(str(self.id))
        if queue_history:
            previous_item_id = queue_history[-1]
            if previous_item_id:
                filters['id__gt'] = previous_item_id

        excludes = {}
        excludes['id__in'] = updated_ids_to_exclude
        ordered_items = self.items.order_by(
            'id').exclude(**excludes)

        next_item = ordered_items.filter(**filters).first()
        if not next_item:
            if self.items.count() > 0:
                next_item = ordered_items.first()

        if next_item:
            if hasattr(next_item, 'queue'):
                slide_route = next_item.queue.get_next_slide_route(
                    ids_to_exclude=updated_ids_to_exclude,
                    historys=historys,
                    path=updated_path,
                )
            elif hasattr(next_item, 'slide'):
                slide = next_item.slide
                slide_route = {
                    'path': updated_path + [slide.id],
                    'slide': slide,
                }
        return slide_route

class Display(TimestampedModel):
    title = models.CharField(max_length=200)
    queue = models.OneToOneField(
        Queue, editable=False, on_delete=models.CASCADE)
                                 
    def __str__(self):
        return "(Display) {}".format(self.title)

class Slide(Item):
    title = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(
        User, blank=True, null=True, editable=False,
        related_name='%(class)s_for_author')
    last_modified_by = models.ForeignKey(
        User, blank=True, null=True, editable=False,
        related_name='%(class)s_for_modifier')
    caption = models.CharField(max_length=200, blank=True)
    render_cfg = models.TextField(blank=True)
    type = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "({}) {}".format(type(self).__name__, self.title)
