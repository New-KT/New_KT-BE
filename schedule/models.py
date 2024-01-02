from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    # 이벤트의 제목을 나타내는 문자열 필드
    title = models.CharField(max_length=255)
    
    # 이벤트의 시작 날짜와 시간을 나타내는 필드
    start = models.DateTimeField()
    
    # 이벤트의 종료 날짜와 시간을 나타내는 필드
    end = models.DateTimeField(null=True, blank=True)
    
    # 이벤트에 대한 추가적인 메모를 저장하는 텍스트 필드 (비어 있을 수 있음)
    memo = models.TextField(blank=True, null=True)
    
    # 이벤트와 관련된 미팅 정보를 저장하는 텍스트 필드 (비어 있을 수 있음)
    meeting = models.BooleanField(default=False)
    
    # 이벤트가 하루 종일인지 여부를 나타내는 부울 필드
    # allDay = models.BooleanField(default=False)
    
    # 이벤트와 연결된 사용자를 나타내는 외래 키
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    
    def __str__(self):
        return self.title