from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from django.conf import settings
from messaging.views import MediaView, ThreadView, MessageView
from messaging.serializers import (
    ThreadSerializer, MessageSerializer, PublicSerializer)
from seed.factories import MediaFactory, ThreadFactory, MessageFactory


class MediaViewTest(APITestCase):
    def test_allowed_methods(self):
        allowed_methods = ['retrieve', 'create']
        for m in allowed_methods:
            self.assertTrue(hasattr(MediaView(), m))

    def test_disallowed_methods(self):
        disallowed_methods = ['list', 'update', 'destroy']
        for m in disallowed_methods:
            self.assertFalse(hasattr(MediaView(), m))

    def test_post(self):
        media = MediaFactory.build()
        image = media.image
        resp = self.client.post(reverse('media-list'), {'image': image})
        self.assertEqual(resp.status_code, 201)


class ThreadViewTest(APITestCase):
    def test_allowed_methods(self):
        allowed_methods = ['retrieve', 'create']
        for m in allowed_methods:
            self.assertTrue(hasattr(ThreadView(), m))

    def test_disallowed_methods(self):
        disallowed_methods = ['list', 'update', 'destroy']
        for m in disallowed_methods:
            self.assertFalse(hasattr(ThreadView(), m))

    def test_post(self):
        thread = ThreadSerializer(instance=ThreadFactory.build())
        data = thread.data.copy()
        del data['messages']  # 'messages' is read-only
        resp = self.client.post(reverse('thread-list'), data)
        self.assertEqual(resp.status_code, 201)


class MessageViewTest(APITestCase):
    def test_allowed_methods(self):
        allowed_methods = ['create']
        for m in allowed_methods:
            self.assertTrue(hasattr(MessageView(), m))

    def test_disallowed_methods(self):
        disallowed_methods = ['retrieve', 'list', 'update', 'destroy']
        for m in disallowed_methods:
            self.assertFalse(hasattr(MessageView(), m))

    def test_post(self):
        msg = MessageSerializer(instance=MessageFactory())
        thread = ThreadFactory()
        data = msg.data.copy()
        data['thread'] = thread.thread_id
        del data['id']
        del data['media']
        data['media'] = MediaFactory().media_id
        resp = self.client.post(reverse('message-list'), data)
        self.assertEqual(resp.status_code, 201)

    def test_invalid_thread_id_post(self):
        msg = MessageSerializer(instance=MessageFactory())
        data = msg.data.copy()
        data['thread'] = 'Invalid value'
        del data['media']
        data['media'] = MediaFactory().media_id
        resp = self.client.post(reverse('message-list'), data)
        self.assertEqual(resp.status_code, 400)

    def test_no_media_provided_post(self):
        msg = MessageSerializer(instance=MessageFactory())
        thread = ThreadFactory()
        data = msg.data.copy()
        data['thread'] = thread.thread_id
        del data['id']
        del data['media']
        resp = self.client.post(reverse('message-list'), data)
        self.assertEqual(resp.status_code, 201)

    def test_thread_closed(self):
        thread = ThreadFactory(closed=True)
        data = MessageSerializer(
            instance=MessageFactory(thread=thread)).data.copy()
        data['thread'] = thread.thread_id
        del data["id"]
        del data["media"]
        resp = self.client.post(reverse('message-list'), data)
        self.assertEqual(resp.status_code, 400)


class PublicViewTest(APITestCase):
    def test_public_thread(self):
        thread = PublicSerializer(instance=ThreadFactory(public=True))
        resp = self.client.get(reverse('messaging_public_threads'))
        self.assertEqual(thread.data, resp.data['results'][0])

    def test_non_public_thread(self):
        ThreadFactory()
        resp = self.client.get(reverse('messaging_public_threads'))
        # Check that 'results' is empty
        self.assertTrue(len(resp.data['results']) == 0)

    def test_pagination(self):
        thread = PublicSerializer(instance=ThreadFactory(public=True))
        ThreadFactory.create_batch(
            settings.REST_FRAMEWORK['PAGE_SIZE'], public=True)
        resp = self.client.get(
            reverse('messaging_public_threads'),
            {'page': 2, 'offset': 100, 'limit': 100}
        )
        self.assertEqual(thread.data, resp.data['results'][0])

    # Test that threads are returned ordered relative to pk descending
    def test_ordering(self):
        thread1 = PublicSerializer(instance=ThreadFactory(public=True))
        PublicSerializer(instance=ThreadFactory(public=True))
        resp = self.client.get(reverse('messaging_public_threads'))
        self.assertEqual(thread1.data, resp.data['results'][1])
