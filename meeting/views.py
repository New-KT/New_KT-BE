from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
import json
from schedule.models import Event
from .models import  Keyword, News 
from datetime import timedelta, datetime
from .ai import meetsum

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MeetingSummaryAPI(APIView):
    
    def get(self, request, *args, **kwargs):
        recent_meeting = Event.objects.filter(user=request.user, meeting=True).latest('start')
        recent_meeting.end = datetime.now()
        
        meetsum.mts(recent_meeting.meeting_text)
        
        return Response({'message': 'Meeting Stopped'}, status=status.HTTP_200_OK)