from django.urls import include, path
from rest_framework.routers import SimpleRouter

from chat.views import ConversationViewSet, MessageViewSet

router = SimpleRouter()
router.register('conversations', ConversationViewSet, basename='conversations')

message_list = MessageViewSet.as_view({'get': 'list'})

urlpatterns = [
    path('', include(router.urls)),
    path('conversations/<uuid:conversation_id>/messages/', message_list, name='message-list'),
]
