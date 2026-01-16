from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from rest_framework_simplejwt.authentication import JWTAuthentication

from chat.models import Conversation, Message


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        user = await self._get_user_from_token()
        if not user:
            await self.close()
            return
        is_participant = await self._is_participant(user, self.conversation_id)
        if not is_participant:
            await self.close()
            return
        self.scope['user'] = user
        self.group_name = f"chat_{self.conversation_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        message_text = content.get('message')
        if not message_text:
            return
        message = await self._create_message(self.scope['user'], self.conversation_id, message_text)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',
                'id': str(message.id),
                'message': message.content,
                'sender': {
                    'id': message.sender_id,
                    'display_name': message.sender.display_name,
                },
                'created_at': message.created_at.isoformat(),
            },
        )

    async def chat_message(self, event):
        await self.send_json(event)

    async def _get_user_from_token(self):
        query_string = self.scope.get('query_string', b'').decode()
        params = parse_qs(query_string)
        token = params.get('token', [None])[0]
        if not token:
            return None
        auth = JWTAuthentication()
        try:
            validated_token = auth.get_validated_token(token)
            user = auth.get_user(validated_token)
        except Exception:
            return None
        return user

    @database_sync_to_async
    def _is_participant(self, user, conversation_id):
        return Conversation.objects.filter(id=conversation_id, participants=user).exists()

    @database_sync_to_async
    def _create_message(self, user, conversation_id, message_text):
        conversation = Conversation.objects.get(id=conversation_id)
        return Message.objects.create(conversation=conversation, sender=user, content=message_text)
