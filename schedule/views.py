

from rest_framework.response import Response
from django.http import JsonResponse

from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import Event
import json
from datetime import datetime
from django.utils import timezone

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GetUserEventsView(APIView):

    def get(self, request, *args, **kwargs):
        user_events = Event.objects.filter(user=request.user)
        event_list = []

        for event in user_events:
            event_data = {
                'id' : event.id,
                'title': event.title,
                'memo': event.memo,
                'start': event.start.strftime('%Y-%m-%dT%H:%M:%S'),
                'end': event.end.strftime('%Y-%m-%dT%H:%M:%S'),
                'meeting': event.meeting,
            }
            event_list.append(event_data)

        print(event_list)
        return JsonResponse({'events': event_list})

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CreateEventView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Content-Type 확인
            if 'application/json' not in request.headers.get('Content-Type', ''):
                return Response({'error': 'Invalid Content-Type. Expected application/json.'}, status=status.HTTP_400_BAD_REQUEST)

            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError as e:
            return Response({'error': f'Invalid JSON format: {e}'}, status=status.HTTP_400_BAD_REQUEST)
        print(request.user)
        title = data.get('title', '')
        memo = data.get('memo', '')
        start_str = data.get('start', '')
        end_str = data.get('end', '')
        meeting = data.get('meeting', False)

        if title and start_str:
            start = datetime.fromisoformat(start_str.rstrip('Z'))
            end = datetime.fromisoformat(end_str.rstrip('Z'))
            start = timezone.make_aware(start, timezone.get_current_timezone())
            end = timezone.make_aware(end, timezone.get_current_timezone())

            event = Event.objects.create(
                title=title,
                memo=memo,
                start=start,
                end=end,
                meeting=meeting,
                user=request.user  # 이 부분은 로그인한 사용자를 기준으로 이벤트를 생성하는 예시입니다.
            )

            event_data = {
                'title': event.title,
                'memo': event.memo,
                'start': event.start.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'end': event.end.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'meeting': event.meeting,
            }

            return Response(event_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Incomplete data or invalid values'}, status=status.HTTP_400_BAD_REQUEST)