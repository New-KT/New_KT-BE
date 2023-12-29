

from rest_framework.response import Response
from django.http import JsonResponse

from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


from .models import Event
import json
from datetime import datetime
from django.utils import timezone

@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
class GetUserEventsView(APIView):

    def get(self, request, *args, **kwargs):
        user_events = Event.objects.filter(user=request.user)
        event_list = []

        for event in user_events:
            event_data = {
                'title': event.title,
                'memo': event.memo,
                'start': event.start.strftime('%Y-%m-%dT%H:%M:%S'),
                'end': event.end.strftime('%Y-%m-%dT%H:%M:%S'),
                'meeting': event.meeting,
            }
            event_list.append(event_data)

        return JsonResponse({'events': event_list})

@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
class CreateEventView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON format: {e}'}, status=400)
        print('데이터', data)
        title = data.get('title', '')
        memo = data.get('memo', '')
        start_str = data.get('start', '')
        end_str = data.get('end', '')
        meeting = data.get('meeting', '')

        if title and start_str:
            
            # start와 end를 DateTimeField에 맞게 변환
            start = datetime.fromisoformat(start_str.rstrip('Z'))
            end = datetime.fromisoformat(end_str.rstrip('Z'))

            # 타임존 정보 추가
            start = timezone.make_aware(start, timezone.get_current_timezone())
            end = timezone.make_aware(end, timezone.get_current_timezone())
            event = Event.objects.create(
                title=title,
                memo=memo,
                start=start,
                end=end,
                meeting=meeting,
                user=request.user
            )
                        # 생성된 이벤트의 정보를 응답
            event_data = {
                'title': event.title,
                'memo': event.memo,
                'start': event.start.strftime('%Y-%m-%dT%H:%M:%SZ'),  # UTC 타임존 사용
                'end': event.end.strftime('%Y-%m-%dT%H:%M:%SZ'),      # UTC 타임존 사용
                'meeting': event.meeting,
            }
            print('event_data', event_data)
            return JsonResponse(event_data,status=201)
        else:
            return JsonResponse({'error': 'Incomplete data'}, status=400)
