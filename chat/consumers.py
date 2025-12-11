import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import Message, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'public_chat' # Sala global por ahora
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope["user"]

        # Unirse a la sala
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        if self.user.is_authenticated:
            # Marcar como Online en Redis (o memoria temporal)
            # En producción, usaríamos Redis directamente. Aquí, simulamos boradcast.
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_status',
                    'user_id': self.user.id,
                    'username': self.user.username,
                    'status': 'online'
                }
            )

    async def disconnect(self, close_code):
        # Salir de la sala
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        if self.user.is_authenticated:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_status',
                    'user_id': self.user.id,
                    'username': self.user.username,
                    'status': 'offline'
                }
            )

    # Recibir mensaje del WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        
        if not self.user.is_authenticated:
            return

        if message:
            # Guardar mensaje (placeholder: en este MVP es chat público efímero o persistente simple)
            # await self.save_message(message) 

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

    async def user_status(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_status',
            'user_id': event['user_id'],
            'username': event['username'],
            'status': event['status']
        }))
