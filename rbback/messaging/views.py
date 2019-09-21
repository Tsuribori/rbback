from rest_framework.parsers import MultiPartParser
from messaging.utils import CreateRetrieveViewSet, CreateViewSet
from messaging.serializers import (
    MediaSerializer, ThreadSerializer, MessageSerializer)
from messaging.models import Media, Thread, Message


class MediaView(CreateRetrieveViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    parser_classes = [MultiPartParser]
    lookup_field = 'media_id'


class ThreadView(CreateRetrieveViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    lookup_field = 'thread_id'


class MessageView(CreateViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
