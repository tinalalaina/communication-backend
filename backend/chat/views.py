from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from chat.models import Conversation, Message
from chat.serializers import ConversationSerializer, MessageSerializer
from friends.models import FriendRequest

User = get_user_model()


class ConversationViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        conversations = Conversation.objects.filter(participants=request.user)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

    def create(self, request):
        other_user_id = request.data.get('user_id')
        if not other_user_id:
            return Response({'detail': 'user_id manquant.'}, status=status.HTTP_400_BAD_REQUEST)
        other_user = User.objects.get(id=other_user_id)
        is_friend = FriendRequest.objects.filter(
            Q(from_user=request.user, to_user=other_user, status='accepted')
            | Q(from_user=other_user, to_user=request.user, status='accepted')
        ).exists()
        if not is_friend:
            return Response({'detail': 'Vous devez être amis pour discuter.'}, status=status.HTTP_403_FORBIDDEN)
        conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.set([request.user, other_user])
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, conversation_id=None):
        messages = Message.objects.filter(conversation_id=conversation_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
