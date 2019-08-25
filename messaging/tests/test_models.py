from django.test import TestCase
from seed.factories import MediaFactory, ThreadFactory, MessageFactory


class MediaModel(TestCase):
    def setUp(self):
        self.media = MediaFactory()

    def test_str(self):
        self.assertEqual(self.media.__str__(), self.media.media_id)

    def test_thumbnail(self):
        self.assertTrue(self.media.thumbnail.width)

    def test_media_id(self):
        self.assertEqual(len(self.media.media_id), 27)


class ThreadModel(TestCase):
    def setUp(self):
        self.thread = ThreadFactory()

    def test_str(self):
        self.assertEqual(
            self.thread.__str__(), self.thread.thread_id)


class MessageModel(TestCase):
    def setUp(self):
        self.message = MessageFactory()

    def test_str(self):
        self.assertEqual(self.message.__str__(), "{}:{}".format(
            str(self.message.date), self.message.post))
