import magic
from django.core.exceptions import ValidationError
from django.conf import settings
from rest_framework import serializers
from messaging.fields import MediaField, ThreadField
from messaging.models import Media, Thread, Message


class MediaSerializer(serializers.ModelSerializer):
    def validate_image(self, value):
        if value.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError(
                'File size too big! Max {} MB allowed.'.format(
                    int(settings.MAX_UPLOAD_SIZE / 1024 / 1024)
                 )
             )

        magic_buffer = bytes(0)
        for chunk in value.chunks():
            magic_buffer += chunk
            if len(magic_buffer) >= 256:
                break
        mime = magic.from_buffer(magic_buffer, mime=True)
        if mime not in settings.ALLOWED_EXTENSIONS:
            raise ValidationError('File type not allowed.')

        return value

    class Meta:
        model = Media
        fields = ('media_id', 'image', 'thumbnail')
        extra_kwargs = {
            'media_id': {'read_only': True},
            'thumbnail': {'read_only': True}
        }


class MessageSerializer(serializers.ModelSerializer):
    thread = ThreadField()
    media = MediaField()

    class Meta:
        model = Message
        fields = ('id', 'date', 'post', 'thread', 'media')


class ThreadSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = (
            'thread_id', 'subject', 'messages')
        extra_kwargs = {
            'url': {'lookup_field': 'thread_id'},
            'thread_id': {'read_only': True}
        }
