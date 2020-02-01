from django.test import TestCase
from django.urls import reverse
from seed.factories import ThreadFactory, UserFactory


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
