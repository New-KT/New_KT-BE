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
from meeting.models import Keyword, News
import json
from datetime import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import traceback
import pytz
from datetime import timedelta


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GetUserEventsView(APIView):

    def get(self, request, *args, **kwargs):
        user_events = Event.objects.filter(user=request.user)
        event_list = []

        for event in user_events:
            event_data = {
                'id': event.id,
                'title': event.title,
                'memo': event.memo,
                'start': (event.start + timedelta(hours=9)).strftime('%Y-%m-%dT%H:%M:%S'),
                'end': (event.end + timedelta(hours=9)).strftime('%Y-%m-%dT%H:%M:%S'),
                'meeting': event.meeting,
            }
            event_list.append(event_data)

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
        start_str = data.get('start', '')
        end_str = data.get('end', '')
        memo = data.get('memo', '')
        meeting = data.get('meeting', False)

        if title and start_str:
            start = datetime.fromisoformat(start_str.rstrip('Z'))
            end = datetime.fromisoformat(end_str.rstrip('Z'))

<<<<<<< HEAD
=======
            # # UTC로 설정된 datetime 객체로 변환
            # start = timezone.make_aware(start, timezone.get_current_timezone())
            # end = timezone.make_aware(end, timezone.get_current_timezone())
>>>>>>> 379f27ee58dc2c71d796ee7349a2d689489dd25f

            # 한국 시간으로 변환
            start_korea = start.astimezone(pytz.timezone('Asia/Seoul'))
            end_korea = end.astimezone(pytz.timezone('Asia/Seoul'))
            
            event = Event.objects.create(
                title=title,
                memo=memo,
                start=start_korea,
                end=end_korea,
                meeting=meeting,
                user=request.user
            )
            
            event_data = {
                'title': event.title,
                'memo': event.memo,
                'start': event.start.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'end': event.end.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'meeting': event.meeting,
            }
            print(event_data)
            return Response(event_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Incomplete data or invalid values'}, status=status.HTTP_400_BAD_REQUEST)
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])

class EventClick(APIView):
    def get(self, request, event_id):
        # event_id에 해당하는 이벤트 가져오기
        event = get_object_or_404(Event, id=event_id)
<<<<<<< HEAD

        # 해당 이벤트의 모든 키워드 가져오기
        keywords = Keyword.objects.filter(meeting=event)

        # 키워드 별로 뉴스 리스트를 담을 리스트 초기화
        response_list = []

        # 키워드에 해당하는 뉴스 리스트 가져오기 및 리스트에 추가
        for keyword in keywords:
            news_list = News.objects.filter(keyword=keyword)
            keyword_data = {
                'keyword': keyword.keyword,
                # 'summary': keyword.news_summary,
                'article_links': [news.link for news in news_list],
                'article_titles': [news.title for news in news_list],
            }
            response_list.append(keyword_data)
=======
        print(event_id)
        event = Event.objects.get(id=event_id)
        print(event)
>>>>>>> 379f27ee58dc2c71d796ee7349a2d689489dd25f

        # 이벤트의 세부 정보를 JSON 형식으로 응답
        if event.meeting:  # meeting이 True일 때
            response_data = {
                'id': event.id,
                'title': event.title,
                'memo': event.memo,
<<<<<<< HEAD
                'start': event.start.strftime('%Y-%m-%dT%H:%M:%S'),
                'end': event.end.strftime('%Y-%m-%dT%H:%M:%S'),
                'meeting': event.meeting,
                'keywords': response_list,
                'summary': '',
=======
                'start': (event.start + timedelta(hours=9)).strftime('%Y-%m-%dT%H:%M:%S'),
                'end': (event.end + timedelta(hours=9)).strftime('%Y-%m-%dT%H:%M:%S'),
                'meeting': event.meeting,
                'keyword': '',
                'summary': '',
                'article_link': '',
                'article_title': ''
>>>>>>> 379f27ee58dc2c71d796ee7349a2d689489dd25f
            }
            print(response_data)
        else:  # meeting이 False일 때
            response_data = {
                'id': event.id,
                'title': event.title,
                'memo': event.memo,
<<<<<<< HEAD
                'start': event.start.strftime('%Y-%m-%dT%H:%M:%S'),
                'end': event.end.strftime('%Y-%m-%dT%H:%M:%S'),
                'meeting': event.meeting,
                'keywords': [],
                'summary': '',
            }
            print(response_data)
        return Response(response_data)
=======
                'start': (event.start + timedelta(hours=9)).strftime('%Y-%m-%dT%H:%M:%S'),
                'end': (event.end + timedelta(hours=9)).strftime('%Y-%m-%dT%H:%M:%S'),
                'meeting': event.meeting
            }
            print(response_data)

        return JsonResponse(response_data)


>>>>>>> 379f27ee58dc2c71d796ee7349a2d689489dd25f



@method_decorator(csrf_exempt, name='dispatch')
class EventDelete(APIView):
    def delete(self, request, event_id):
        try:
            event = get_object_or_404(Event, id=event_id)
            print(f"Event to be deleted: {event}")

            # 삭제 권한 확인 (예: 현재 로그인한 사용자와 일정의 소유자를 비교)
            if not request.user.is_authenticated or request.user != event.user:
                return JsonResponse({'error': '권한이 없습니다.'}, status=403)

            # 일정 삭제
            event.delete()

            return JsonResponse({'message': '일정이 성공적으로 삭제되었습니다.'})

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print(traceback.format_exc())
            return JsonResponse({'error': '서버 오류가 발생했습니다.'}, status=500)

   
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])       
class LoginHomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 현재 시간 기준으로 가장 가까운 일정만 가져오도록 로직을 추가
        now = timezone.now()
        closest_event = Event.objects.filter(end__gte=now).order_by('start').first()

        if closest_event:
            # 필요한 정보를 JSON 형식으로 응답
            response_data = {
                'id': closest_event.id,
                'title': closest_event.title,
                'start': closest_event.start.isoformat(),
                'end': closest_event.end.isoformat(),
                'memo': closest_event.memo,
            }
            return Response(response_data)
        else:
            # 일정이 없는 경우 응답
            return Response({'message': 'No upcoming events'}, status=204)