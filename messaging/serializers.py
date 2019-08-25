from messaging.models import Media, Thread, Message
from rest_framework import serializers
from messaging.fields import MediaField, ThreadField


class MediaSerializer(serializers.ModelSerializer):
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
