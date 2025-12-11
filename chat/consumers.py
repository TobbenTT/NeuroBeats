import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import Message, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.conversation_id}'
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        # Verificar si el usuario pertenece a la conversación
        if not await self.can_access_conversation(self.conversation_id, self.user):
            await self.close()
            return

        # Unirse a la sala
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Salir de la sala
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Recibir mensaje del WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        
        if not self.user.is_authenticated:
            return

        if message:
            # Guardar mensaje en base de datos
            await self.save_message(self.conversation_id, self.user, message) 

            # Enviar mensaje al grupo
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': self.user.username,
                    'avatar_url': self.user.profile.avatar.url if hasattr(self.user, 'profile') else '',
                    'timestamp': str(timezone.now().strftime("%H:%M"))
                }
            )

    # Manejar mensaje del grupo
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'username': event['username'],
            'avatar_url': event['avatar_url'],
            'timestamp': event['timestamp']
        }))

    @database_sync_to_async
    def can_access_conversation(self, conversation_id, user):
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            return conversation.participants.filter(id=user.id).exists()
        except Conversation.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, conversation_id, user, content):
        conversation = Conversation.objects.get(id=conversation_id)
        return Message.objects.create(conversation=conversation, sender=user, content=content)
