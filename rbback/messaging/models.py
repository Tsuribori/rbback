import uuid
import os
from io import BytesIO
from django.db import models
from django.core.files.base import ContentFile
from django.conf import settings
from PIL import Image
from messaging.utils import IDSigner


def get_image_name(instance, filename):
    return 'image/{}/{}'.format(instance.media_id, filename)


def get_thumb_name(instance, filename):
    return 'thumbnail/{}/{}'.format(instance.media_id, filename)


class Media(models.Model, IDSigner):
    media_id = models.CharField(max_length=27, unique=True)
    image = models.ImageField(upload_to=get_image_name)
    thumbnail = models.ImageField(upload_to=get_thumb_name)

    def save(self, *args, **kwargs):
        self.media_id = self.sign_id(uuid.uuid4())
        if self.image:
            self.make_thumbnail()
        super(Media, self).save(*args, **kwargs)

    def __str__(self):
        return self.media_id

    def make_thumbnail(self):
        image = Image.open(self.image)
        thumb_size = (500, 500)
        image.thumbnail(thumb_size, Image.ANTIALIAS)

        thumb_name, _ = os.path.splitext(self.image.name)
        thumb_filename = thumb_name + '.jpg'

        temp_thumb = BytesIO()
        image.save(
            temp_thumb,
            image.format,
            quality=10,
            optimize=True
        )
        temp_thumb.seek(0)

        self.thumbnail.save(
            thumb_filename,
            ContentFile(temp_thumb.read()),
            save=False)
        temp_thumb.close()


class Thread(models.Model, IDSigner):
    subject = models.CharField(max_length=100, blank=False)
    thread_id = models.CharField(max_length=27, unique=True, blank=False)
    closed = models.BooleanField(default=False)
    public = models.BooleanField(default=False)

    def __str__(self):
        return "{}: {}".format(self.thread_id, self.subject)

    def save(self, *args, **kwargs):
        if not self.thread_id:
            uuid_id = uuid.uuid4()
            self.thread_id = self.sign_id(uuid_id)
        super(Thread, self).save(*args, **kwargs)


class Message(models.Model):
    date = models.DateTimeField(auto_now=True)
    post = models.TextField(max_length=10000, blank=False)
    media = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages')
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return "{}:{}".format(str(self.date), self.post)

    def save(self, *args, **kwargs):
        if not self.thread.closed:
            if self.thread.messages.count() >= settings.MAX_POSTS:
                self.thread.closed = True
                self.thread.save()
            super(Message, self).save(*args, **kwargs)

    class Meta:
        ordering = ['pk']
