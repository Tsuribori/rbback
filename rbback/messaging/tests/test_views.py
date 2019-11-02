from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from messaging.views import MediaView, ThreadView, MessageView
from messaging.serializers import ThreadSerializer, MessageSerializer
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

    def test_invalid_media_post(self):
        msg = MessageSerializer(instance=MessageFactory())
        thread = ThreadFactory()
        data = msg.data.copy()
        data['thread'] = thread.thread_id
        del data['id']
        del data['media']
        resp = self.client.post(reverse('message-list'), data)
        self.assertEqual(resp.status_code, 400)
