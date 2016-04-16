from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from spotlights.models import Display, Queue, ImageSlide, UrlSlide, QueueItem


class Command(BaseCommand):
    help = 'Creates fixture data for django-spotlights'

    def handle(self, *args, **options):
        with transaction.atomic():
            users = self.generate_users()
            displays = self.generate_displays()
            slides = self.generate_slides(users=users)
            queues = self.generate_queues()
            queueitems = self.generate_queueitems(
                displays=displays,
                slides=slides,
                queues=queues
            )
        self.stdout.write(self.style.SUCCESS("done!"))

    def generate_displays(self, num_displays=3):
        displays = {}
        for i in range(3):
            title = "display-{}".format(i)
            queue = Queue(title="queue_for_display_{}".format(title))
            queue.save()
            display = Display(
                title=title,
                queue=queue
            )
            display.save()
            displays[display.id] = display
        return displays

    def generate_users(self, num_users=3):
        users = {}
        for i in range(num_users):
            username = "user-{}".format(i)
            user = User(
                username=username,
                is_staff=True,
            )
            user.set_password(username)
            user.save()
            users[user.id] = user
        return users

    def generate_slides(self, num_slides=10, slide_classes=None, users=None):
        slides = {}
        if not slide_classes:
            slide_classes = [
                ImageSlide,
                UrlSlide
            ]
        num_slide_classes = len(slide_classes)
        users_list = list(users.values())
        num_users = len(users_list)
        for i in range(num_slides):
            slide_class = slide_classes[i % num_slide_classes]
            title = "slide-{}".format(i)
            caption = "caption-{}".format(i)
            author = users_list[i % num_users]
            slide = self.generate_slide(
                index=i,
                slide_class=slide_class,
                title=title,
                caption=caption,
                author=author,
            )
            slide.save()
            slides[slide.id] = slide
        return slides

    def generate_slide(self, index=0, slide_class=None, **kwargs):
        generator_name = "generate_{}".format(slide_class.__name__)
        generator = getattr(self, generator_name, lambda: None)
        return generator(index=index, **kwargs)

    def generate_ImageSlide(self, index=None, **kwargs):
        return ImageSlide(**kwargs)

    def generate_UrlSlide(self, index=None, **kwargs):
        return UrlSlide(**kwargs)

    def generate_queues(self, num_queues=3):
        queues = {}
        for i in range(num_queues):
            queue = Queue(title="queue-{}".format(i))
            queue.save()
            queues[queue.id] = queue
        return queues

    def generate_queueitems(self, num_queueitems=10, displays={}, queues={},
                            slides={}):
        queueitems = {}
        queues_list = (
            [display.queue for display in list(displays.values())] + 
            list(queues.values())
        )
        num_queues = len(queues_list)

        items_list = list(slides.values()) + queues_list
        num_items = len(items_list)

        for i in range(num_queueitems):
            queue = queues_list[i % num_queues]
            item = None
            for j in range(i, i + num_items):
                item = items_list[j % num_items]
                if item is not queue:
                    break
            queueitem = QueueItem(
                queue=queue,
                item_content_type=ContentType.objects.get_for_model(item),
                item_id=item.id
            )
            queueitem.save()
            queueitems[queueitem.id] = queueitem
        return queueitems
