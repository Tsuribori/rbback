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
            self.thread.__str__(),
            "{}: {}".format(self.thread.thread_id, self.thread.subject)
        )


class MessageModel(TestCase):
    def setUp(self):
        self.message = MessageFactory()

    def test_str(self):
        self.assertEqual(self.message.__str__(), "{}:{}".format(
            str(self.message.date), self.message.post))

    def test_no_post_when_thread_closed(self):
        thread = ThreadFactory()
        MessageFactory.create_batch(16, thread=thread)
        thread.refresh_from_db()
        self.assertTrue(thread.closed)
