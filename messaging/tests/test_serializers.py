from rest_framework.test import APITestCase
from messaging.serializers import (
    MediaSerializer, ThreadSerializer, MessageSerializer)
from seed.factories import ThreadFactory, MessageFactory


class MediaSerializerTest(APITestCase):
    def setUp(self):
        self.extra_kwargs = MediaSerializer.Meta.extra_kwargs

    def test_thumbnail_read_only(self):
        self.assertTrue(self.extra_kwargs['thumbnail']['read_only'])

    def test_media_id_read_only(self):
        self.assertTrue(self.extra_kwargs['media_id']['read_only'])


class ThreadSerializerTest(APITestCase):
    def test_thread_id_read_only(self):
        extra_kwargs = ThreadSerializer.Meta.extra_kwargs
        read_only = extra_kwargs['thread_id']['read_only']
        self.assertTrue(read_only)

    def test_message_nested(self):
        thread = ThreadFactory()
        message = MessageFactory(thread=thread)
        thread_serializer = ThreadSerializer(instance=thread)
        message_serializer = MessageSerializer(instance=message)
        self.assertEqual(
            thread_serializer.data['messages'][0], message_serializer.data)


class MessageSerializerTest(APITestCase):
    def test_thread_write_only(self):
        serializer = MessageSerializer(instance=MessageFactory())
        self.assertFalse('thread' in serializer.data)
