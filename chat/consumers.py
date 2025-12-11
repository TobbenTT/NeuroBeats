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
        action_type = text_data_json.get('type', 'chat_message') # default to chat_message
        
        if not self.user.is_authenticated:
            return

        if action_type == 'chat_message':
            message = text_data_json.get('message')
            if message:
                # Guardar mensaje en base de datos
                saved_msg = await self.save_message(self.conversation_id, self.user, message) 

                # Enviar mensaje al grupo (LIVE CHAT)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'username': self.user.username,
                        'avatar_url': self.user.profile.avatar.url if hasattr(self.user, 'profile') else '',
                        'timestamp': saved_msg.timestamp.strftime("%H:%M"),
                        'message_id': saved_msg.id,
                        'sender_id': self.user.id
                    }
                )
                
                # --- SEND NOTIFICATION TO OTHERS ---
                other_participants = await self.get_other_participants(self.conversation_id, self.user.id)
                # Debug Check
                print(f"DEBUG NOTIF: Sender={self.user.id}, Others={other_participants}")
                
                for participant_id in other_participants:
                    await self.channel_layer.group_send(
                        f"user_{participant_id}",
                        {
                            'type': 'send_notification',
                            'notification': {
                                'type': 'new_message',
                                'from_user': self.user.username,
                                'content': message[:30] + '...' if len(message) > 30 else message,
                                'url': f'/chat/{self.conversation_id}/' 
                            }
                        }
                    )

        elif action_type == 'mark_read':
            # El usuario actual ha leído los mensajes de la conversación
            await self.mark_conversation_as_read(self.conversation_id, self.user)
            
            # Avisar al grupo que se leyeron (para poner el doble check azul)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'messages_read',
                    'reader_id': self.user.id
                }
            )

    # Manejar mensaje del grupo
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def messages_read(self, event):
        await self.send(text_data=json.dumps(event))

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

    @database_sync_to_async
    def mark_conversation_as_read(self, conversation_id, user):
        conversation = Conversation.objects.get(id=conversation_id)
        # Marcar como leídos los mensajes que NO son míos
        conversation.messages.exclude(sender=user).filter(is_read=False).update(is_read=True)

    @database_sync_to_async
    def get_other_participants(self, conversation_id, user_id):
        conversation = Conversation.objects.get(id=conversation_id)
        return list(conversation.participants.exclude(id=user_id).values_list('id', flat=True))

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            await self.close()
            return

        self.group_name = f"user_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event['notification']))
