from django.test import TestCase
from django.urls import reverse
from django.contrib.admin.sites import AdminSite
from messaging.models import Message
from messaging.admin import MessageAdmin
from seed.factories import ThreadFactory, MessageFactory, UserFactory


class ThreadAdmin(TestCase):
    def setUp(self):
        user = UserFactory()
        self.client.force_login(user)

    def test_hide_thread(self):
        thread = ThreadFactory(public=True)
        data = {'action': 'hide_thread',
                '_selected_action': [thread.pk, ]}
        change_url = reverse('admin:messaging_thread_changelist')
        self.client.post(change_url, data)
        thread.refresh_from_db()
        self.assertFalse(thread.public)

    def test_message_ordering(self):
        MessageFactory()
        message = MessageFactory()
        message_admin = MessageAdmin(model=Message, admin_site=AdminSite())
        messages = message_admin.get_queryset(request=None)
        self.assertEqual(messages[0], message)
