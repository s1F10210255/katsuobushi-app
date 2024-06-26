from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.csrf import csrf_exempt
import urllib
import json

from .models import Reply

import random


WEBHOOK_URL = 'https://hooks.slack.com/services/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'
VERIFICATION_TOKEN = 'Wu45KWZMrrVjNz8FZ9xp6Qqx'
ACTION_HOW_ARE_YOU = 'HOW_ARE_YOU'

def index(request):
    positive_replies = Reply.objects.filter(response=Reply.POSITIVE)
    neutral_replies = Reply.objects.filter(response=Reply.NEUTRAL)
    negative_replies = Reply.objects.filter(response=Reply.NEGATIVE)

    context = {
        'positive_replies': positive_replies,
        'neutral_replies': neutral_replies,
        'negative_replies': negative_replies,

    }
    return render(request, 'index.html', context)

def clear(request):
    Reply.objects.all().delete()
    return redirect(index)

def announce(request):
    if request.method == 'POST':
        data = {
            'text': request.POST['message']
        }
        post_message(WEBHOOK_URL, data)

    return redirect(index)

@csrf_exempt
def echo(request):
    if request.method != 'POST':
        return JsonResponse({})
    
    if request.POST.get('token') != VERIFICATION_TOKEN:
        raise SuspiciousOperation('Invalid request.')
    
    user_name = request.POST['user_name']
    user_id = request.POST['user_id']
    content = request.POST['text']

    result = {
        'text': '<@{}> {}'.format(user_id, content.upper()),
        'response_type': 'in_channel'
    }

    return JsonResponse(result)

@csrf_exempt
def hello(request):
    if request.method != 'POST':
        return JsonResponse({})
    
    if request.POST.get('token') != VERIFICATION_TOKEN:
        raise SuspiciousOperation('Invalid request.')
    
    user_name = request.POST['user_name']
    user_id = request.POST['user_id']
    content = request.POST['text']

    result = {
        'blocks': [
            {
                'type' : 'section',
                'text' : {
                    'type': 'mrkdwn',
                    'text': '<@{}> 今日の気分は?'.format(user_id)
                },
                'accessory': {
                    'type': 'static_select',
                    'placeholder': {
                        'type': 'plain_text',
                        'text': 'I am:',
                        'emoji': True
                    },
                    'options': [
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'Fine.',
                                'emoji': True
                            },
                            'value': 'positive'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'So so.',
                                'emoji': True
                            },
                            'value': 'neutral'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'Terrible.',
                                'emoji': True
                            },
                            'value': 'negative'
                        }
                    ],
                    'action_id': ACTION_HOW_ARE_YOU
                }
            }
        ],
        'response_type': 'in_channel'
    }

    return JsonResponse(result)

@csrf_exempt
def reply(request):
    if request.method != 'POST':
        return JsonResponse({})
    
    payload = json.loads(request.POST.get('payload'))
    print(payload)
    if payload.get('token') != VERIFICATION_TOKEN:
        raise SuspiciousOperation('Invalid request.')
    
    if payload['actions'][0]['action_id'] != ACTION_HOW_ARE_YOU:
        raise SuspiciousOperation('Invalid request.')
    
    user = payload['user']
    selected_value = payload['actions'][0]['selected_option']['value']
    response_url = payload['response_url']

    if selected_value == 'positive':
        reply = Reply(user_name=user['name'], user_id=user['id'], response=Reply.POSITIVE)
        reply.save()
        response = {
            'text': '<@{}> シチュー！ :stew:'.format(user['id'])
        }
    elif selected_value == 'neutral':
        reply = Reply(user_name=user['name'], user_id=user['id'], response=Reply.NEUTRAL)
        reply.save()
        response = {
            'text': '<@{}> 寿司！ :sushi:'.format(user['id'])
        }
    else:
        reply = Reply(user_name=user['name'], user_id=user['id'], response=Reply.NEGATIVE)
        reply.save()
        response = {
            'text': '<@{}> 餃子！ :dumpling:'.format(user['id'])
        }
    
    post_message(response_url, response)
    return JsonResponse({})

def post_message(url, data):
    headers = {
        'Content-Type': 'application/json',
    }
    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()




@csrf_exempt
def katsuobushi(request):
    if request.method != 'POST':
        return JsonResponse({})
    
    if request.POST.get('token') != VERIFICATION_TOKEN:
        raise SuspiciousOperation('Invalid request.')
    
    user_name = request.POST['user_name']
    user_id = request.POST['user_id']
    content = request.POST['text']
    result = {
        'blocks': [
            {
                'type' : 'section',
                'text' : {
                    'type': 'mrkdwn',
                    'text': '<@{}> What is the best menu for tonight?'.format(user_id)
                },
                'accessory': {
                    'type': 'static_select',
                    'placeholder': {
                        'type': 'plain_text',
                        'text': '気分は？:',
                        'emoji': True
                    },
                    'options': [
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': '洋食?',
                                'emoji': True
                            },
                            'value': 'positive'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': '和食?',
                                'emoji': True
                            },
                            'value': 'neutral'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': '中華?',
                                'emoji': True
                            },
                            'value': 'negative'
                        }
                    ],
                    'action_id': ACTION_HOW_ARE_YOU
                }
            }
        ],
        'response_type': 'in_channel'
    }

    return JsonResponse(result)

@csrf_exempt
def charm(request):
    result =Reply(random.choice(['大吉', '吉', '中吉', '小吉', '末吉', '凶', '大凶']),response=Reply.POSITIVE)
    return result
