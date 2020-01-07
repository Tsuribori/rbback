from rest_framework.test import APITestCase
from messaging.serializers import (
    MediaSerializer, ThreadSerializer, MessageSerializer, PublicSerializer)
from seed.factories import ThreadFactory, MessageFactory


class MediaSerializerTest(APITestCase):
    def setUp(self):
        self.extra_kwargs = MediaSerializer.Meta.extra_kwargs

    def test_thumbnail_read_only(self):
        self.assertTrue(self.extra_kwargs['thumbnail']['read_only'])

    def test_media_id_read_only(self):
        self.assertTrue(self.extra_kwargs['media_id']['read_only'])


class ThreadSerializerTest(APITestCase):
    def setUp(self):
        self.extra_kwargs = ThreadSerializer.Meta.extra_kwargs

    def test_thread_id_read_only(self):
        read_only = self.extra_kwargs['thread_id']['read_only']
        self.assertTrue(read_only)

    def test_closed_read_only(self):
        read_only = self.extra_kwargs['closed']['read_only']
        self.assertTrue(read_only)

    def test_message_nested(self):
        thread = ThreadFactory()
        message = MessageFactory(thread=thread)
        thread_serializer = ThreadSerializer(instance=thread)
        message_serializer = MessageSerializer(instance=message)
        self.assertEqual(
            thread_serializer.data['messages'][0], message_serializer.data)

    def test_message_count(self):
        thread = ThreadFactory()
        MessageFactory(thread=thread)
        thread_serializer = ThreadSerializer(instance=thread)
        self.assertEqual(thread_serializer.data['message_count'], 1)

    # Test that nested messages are in order relating to pk ascending
    def test_message_ordering(self):
        thread = ThreadFactory()
        message = MessageFactory(thread=thread)
        MessageFactory(thread=thread)
        thread_serializer = ThreadSerializer(instance=thread)
        self.assertEqual(
            thread_serializer.data['messages'][0]['id'], message.id)


class MessageSerializerTest(APITestCase):
    def test_thread_write_only(self):
        serializer = MessageSerializer(instance=MessageFactory())
        self.assertFalse('thread' in serializer.data)

    def test_thread_closed(self):
        thread = ThreadFactory(closed=True)
        serializer = MessageSerializer(data=MessageFactory(thread=thread))
        self.assertFalse(serializer.is_valid())


class PublicSerializerTest(APITestCase):
    def test_no_messages(self):
        fields = PublicSerializer.Meta.fields
        self.assertFalse('messages' in fields)
