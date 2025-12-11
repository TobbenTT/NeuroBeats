from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Conversation

User = get_user_model()

@login_required
def conversations_list(request):
    conversations = request.user.conversations.all().order_by('-created_at')
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
    else:
        # Create new conversation
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, target_user)
    
    # If HTMX (from popup), render the detail partial directly
    if request.headers.get('HX-Request'):
        messages = conversation.messages.all().order_by('timestamp')
        return render(request, 'chat/partials/conversation_detail_partial.html', {
            'conversation': conversation, 
            'messages': messages,
            'current_user': request.user
        })
        
    return redirect('conversation_detail', conversation_id=conversation.id)
