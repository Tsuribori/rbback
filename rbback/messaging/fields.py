import json
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from messaging.models import Media, Thread


class ThreadField(serializers.RelatedField):
    def __init__(self, *args, **kwargs):
        self.queryset = Thread.objects.all()
        super(ThreadField, self).__init__(write_only=True, *args, **kwargs)

    def to_representation(self, value):
        return value.thread_id

    def to_internal_value(self, data):
        try:
            thread = Thread.objects.get(thread_id=data)
            return thread
        except Thread.DoesNotExist:
            raise ValidationError('Thread not found.')


class MediaField(serializers.Field):
    def __init__(self, *args, **kwargs):
        self.queryset = Media.objects.all()
        super(MediaField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        # return messaging.serializers.MediaSerializer(instance=value).data
        json_dict = {
            'thumbnail': value.thumbnail.url,
            'image': value.image.url
        }
        return json_dict

    def to_internal_value(self, data):
        try:
            media = Media.objects.get(media_id=data)
            return media
        except Media.DoesNotExist:
            raise ValidationError('Media not found.')
