from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Conversation

User = get_user_model()

from django.db.models import Max, OuterRef, Subquery
from .models import Conversation, Message

@login_required
def conversations_list(request):
    # Subquery to get the last message for each conversation
    last_message_subquery = Message.objects.filter(
        conversation=OuterRef('pk')
    ).order_by('-timestamp')

    conversations = request.user.conversations.exclude(
        hidden_by=request.user
    ).annotate(
        last_msg_content=Subquery(last_message_subquery.values('content')[:1]),
        last_msg_time=Subquery(last_message_subquery.values('timestamp')[:1])
    ).order_by('-last_msg_time')
    
    template = 'chat/partials/conversation_list_partial.html' if request.headers.get('HX-Request') else 'chat/conversations_list.html'
    return render(request, template, {'conversations': conversations})

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Security check: ensure user is a participant
    if request.user not in conversation.participants.all():
        return redirect('conversations_list')
        
    messages = conversation.messages.all().order_by('timestamp')
    
    template = 'chat/partials/conversation_detail_partial.html' if request.headers.get('HX-Request') else 'chat/conversation_detail.html'
    
    return render(request, template, {
        'conversation': conversation, 
        'messages': messages,
        'current_user': request.user
    })

@login_required
def start_chat(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    
    if target_user == request.user:
        return redirect('conversations_list')
        
    # Check if conversation already exists
    conversations = Conversation.objects.filter(participants=request.user).filter(participants=target_user)
    
    if conversations.exists():
        conversation = conversations.first()
        # Revive conversation if hidden
        if request.user in conversation.hidden_by.all():
            conversation.hidden_by.remove(request.user)
    else:
        # Create new conversation
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, target_user)
    
    # If HTMX (from popup), render the detail partial directly
    if request.headers.get('HX-Request'):
        from .models import ChatClearHistory
        last_clear = ChatClearHistory.objects.filter(conversation=conversation, user=request.user).first()
        if last_clear:
             messages = conversation.messages.filter(timestamp__gt=last_clear.cleared_at).order_by('timestamp')
        else:
             messages = conversation.messages.all().order_by('timestamp')
             
        return render(request, 'chat/partials/conversation_detail_partial.html', {
            'conversation': conversation, 
            'messages': messages,
            'current_user': request.user
        })
        
    return redirect('conversation_detail', conversation_id=conversation.id)

@login_required
def leave_conversation(request, conversation_id):
    if request.method == 'POST':
        conversation = get_object_or_404(Conversation, id=conversation_id)
        if request.user in conversation.participants.all():
            # SOFT DELETE / CLEAR HISTORY
            from .models import ChatClearHistory
            from django.utils import timezone
            
            # Update or create the clear history record
            ChatClearHistory.objects.update_or_create(
                conversation=conversation,
                user=request.user,
                defaults={'cleared_at': timezone.now()}
            )
            
            # Also hide it from the list
            conversation.hidden_by.add(request.user)
            
            # If HTMX, return the conversations list to swap the content
            if request.headers.get('HX-Request'):
                 return conversations_list(request)
                 
        return redirect('conversations_list')
    return redirect('conversations_list')


