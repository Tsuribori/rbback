import os
import factory
from messaging.models import Media, Thread, Message


class MediaFactory(factory.DjangoModelFactory):
    class Meta:
        model = Media

    image = factory.django.ImageField(from_path=os.path.join(
         os.path.dirname(os.path.abspath(__file__)), 'meadow.png'))


class ThreadFactory(factory.DjangoModelFactory):
    class Meta:
        model = Thread
        django_get_or_create = ('thread_id',)

    subject = 'Thread for testing'
    thread_id = factory.Sequence(lambda n: str(n))


class MessageFactory(factory.DjangoModelFactory):
    class Meta:
        model = Message

    date = factory.Faker('date_time')
    post = 'Test post'
    thread = factory.SubFactory(ThreadFactory)
    media = factory.SubFactory(MediaFactory)
