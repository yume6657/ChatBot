from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Conversation, Message, UserProfile
from .deepseek_api import DeepSeekAPI
import json


def home(request):
    """首页"""
    return render(request, 'index.html')


def register(request):
    """用户注册"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('chat')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    """用户登录"""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('chat')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    """用户登出"""
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')


@login_required
def chat_view(request):
    """聊天界面"""
    conversations = Conversation.objects.filter(user=request.user)
    return render(request, 'chat.html', {'conversations': conversations})


@login_required
def get_conversations(request):
    """获取用户的所有对话"""
    conversations = Conversation.objects.filter(user=request.user)
    data = [
        {
            'id': conv.id,
            'title': conv.title,
            'created_at': conv.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': conv.updated_at.strftime('%Y-%m-%d %H:%M'),
            'message_count': conv.messages.count()
        }
        for conv in conversations
    ]
    return JsonResponse(data, safe=False)


@login_required
def get_messages(request, conversation_id):
    """获取特定对话的消息"""
    try:
        conversation = Conversation.objects.get(id=conversation_id, user=request.user)
        messages = conversation.messages.all()
        data = [
            {
                'id': msg.id,
                'role': msg.role,
                'content': msg.content,
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M'),
                'tokens_used': msg.tokens_used
            }
            for msg in messages
        ]
        return JsonResponse(data, safe=False)
    except Conversation.DoesNotExist:
        return JsonResponse({'error': '对话不存在'}, status=404)


@csrf_exempt
@login_required
def send_message(request):
    """发送消息到DeepSeek API"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message_content = data.get('message', '').strip()
            conversation_id = data.get('conversation_id')
            
            if not message_content:
                return JsonResponse({'error': '消息内容不能为空'}, status=400)
            
            if conversation_id:
                conversation = Conversation.objects.get(id=conversation_id, user=request.user)
            else:
                conversation = Conversation.objects.create(
                    user=request.user,
                    title=message_content[:50] + '...' if len(message_content) > 50 else message_content
                )
            
            user_message = Message.objects.create(
                conversation=conversation,
                role='user',
                content=message_content,
                tokens_used=DeepSeekAPI().estimate_tokens(message_content)
            )
            
            previous_messages = conversation.messages.all()[:10]
            messages_for_api = [
                {
                    'role': msg.role,
                    'content': msg.content
                }
                for msg in previous_messages
            ]
            
            deepseek = DeepSeekAPI()
            result = deepseek.send_message(messages_for_api)
            
            if result['success']:
                assistant_message = Message.objects.create(
                    conversation=conversation,
                    role='assistant',
                    content=result['content'],
                    tokens_used=result['tokens_used']
                )
                
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile.total_tokens_used += result['tokens_used']
                user_profile.save()
                
                return JsonResponse({
                    'success': True,
                    'conversation_id': conversation.id,
                    'assistant_message': {
                        'id': assistant_message.id,
                        'content': assistant_message.content,
                        'timestamp': assistant_message.timestamp.strftime('%Y-%m-%d %H:%M')
                    },
                    'tokens_used': result['tokens_used']
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': result['error']
                }, status=500)
                
        except Conversation.DoesNotExist:
            return JsonResponse({'error': '对话不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'服务器错误: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': '只支持POST请求'}, status=405)


@csrf_exempt
@login_required
def create_conversation(request):
    """创建新对话"""
    if request.method == 'POST':
        conversation = Conversation.objects.create(
            user=request.user,
            title='新对话'
        )
        return JsonResponse({
            'id': conversation.id,
            'title': conversation.title,
            'created_at': conversation.created_at.strftime('%Y-%m-%d %H:%M')
        })
    else:
        return JsonResponse({'error': '只支持POST请求'}, status=405)


@csrf_exempt
@login_required
def delete_conversation(request, conversation_id):
    """删除对话"""
    if request.method == 'POST':
        try:
            conversation = Conversation.objects.get(id=conversation_id, user=request.user)
            conversation.delete()
            return JsonResponse({'success': True})
        except Conversation.DoesNotExist:
            return JsonResponse({'error': '对话不存在'}, status=404)
    else:
        return JsonResponse({'error': '只支持POST请求'}, status=405)


@login_required
def get_user_stats(request):
    """获取用户统计信息"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    total_conversations = Conversation.objects.filter(user=request.user).count()
    total_messages = Message.objects.filter(conversation__user=request.user).count()
    
    return JsonResponse({
        'total_tokens_used': user_profile.total_tokens_used,
        'total_conversations': total_conversations,
        'total_messages': total_messages
    })