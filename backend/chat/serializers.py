from rest_framework import serializers

from chat.models import Conversation, Message
from users.serializers import UserPublicSerializer


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserPublicSerializer(read_only=True, many=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserPublicSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'created_at']
        read_only_fields = ['id', 'conversation', 'sender', 'created_at']
