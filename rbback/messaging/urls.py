from django.urls import path, include
from rest_framework import routers
from messaging.views import MediaView, ThreadView, MessageView, PublicListView


router = routers.DefaultRouter()
router.register(r'media', MediaView, base_name='media')
router.register(r'thread', ThreadView, base_name='thread')
router.register(r'message', MessageView, base_name='message')

urlpatterns = [
    path('', include(router.urls)),
    path('public/', PublicListView.as_view(), name='messaging_public_threads')
]
