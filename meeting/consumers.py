
import json, asyncio, time, sys, re, pyaudio, queue
from google.cloud import speech
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .ai import stt_save_file
from meeting.ai.key import *
from meeting.ai.crawling_main import *
from meeting.ai.meetsum import *

from datetime import datetime, timedelta
from schedule.models import Event
from meeting.models import Keyword, News
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
class AudioConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stt_running = True
        self.total_data = None
        
    async def connect(self):

        try:
            # WebSocket 쿼리 매개변수에서 token 추출
            token = self.scope.get('query_string').decode('utf-8').split('=')[1]

            # Token 모델을 사용하여 유저를 가져오기
            user = await self.get_user_from_token(token)

            if user:
                self.user = user
                await self.accept()
            else:
                await self.close()

        except Exception as e:
            print(f"Error connecting: {e}")

    async def disconnect(self, close_code):
        pass

    async def stt(self):
        print('stt 실행됨')
        print('self.stt_running', self.stt_running)
        total = []
   
        RATE = 16000
        CHUNK = int(RATE / 10)  # 100ms
        
        language_code = 'ko-KR'
        client = speech.SpeechClient()
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=language_code)
        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True)

        start_datetime = datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
        start_datetime = start_datetime.replace(microsecond=0)
        end_meeting= start_datetime + timedelta(minutes=20) 
        start_meeting = start_datetime - timedelta(minutes=20)  
            
        # 주어진 시간 범위에 미팅이 있는지 확인(Meeting인 경우에만 가져옴)
        meetings_in_range = await database_sync_to_async(
            lambda: Event.objects.filter(
                user=self.user, meeting=True, start__range=[start_meeting, end_meeting]
            ).exists()
        )()

        if meetings_in_range:
            meeting = await database_sync_to_async(
                lambda: Event.objects.filter(
                    user=self.user, meeting=True, start__range=[start_meeting, end_meeting]
                ).first()
            )()
            meeting.start = start_datetime
            await database_sync_to_async(meeting.save)()
        else:
            meeting = await database_sync_to_async(
                Event.objects.create)(
                    title='회의',
                    start=start_datetime,
                    end=start_datetime + timedelta(minutes=40),
                    memo='',
                    meeting=True,
                    user=self.user,
                    summary='',
            )
        
        output_file_path = f"meeting_{start_datetime.month}_{start_datetime.day}_{start_datetime.hour}_{start_datetime.minute}.txt"
        
        keywords_list=[]
        with open(output_file_path, 'a+', encoding='utf-8') as output_file:
            with stt_save_file.MicrophoneStream(RATE, CHUNK) as stream:
                audio_generator = stream.generator()
                requests = (speech.StreamingRecognizeRequest(audio_content=content)
                            for content in audio_generator)

                responses = client.streaming_recognize(streaming_config, requests)

                start_time = time.time()
                
                for response in responses:
                    
                    stt_save_file.listen_print_loop(response, output_file)
                    if time.time() - start_time >= 60:
                        output_file.seek(0) 
                        meeting_text = output_file.read().replace('\n', ' ')
                        
                        print("Before keyword() call")
                        print('meeting_text', meeting_text)
                        # keywords_list = keyword(output_file_path, keywords_list)
                        keywords_list = keyword2(meeting_text, keywords_list)
                        print("After keyword() call")

                        for word in keywords_list[-2:]:
                            print(word)
                            result = await crawl(word)
                            print('After crawl() call')
                            
                            keyword_instance = await database_sync_to_async(Keyword.objects.create)(
                                meeting=meeting, keyword=word, news_summary=result[0]['news_summary']
                            )
                            for i in range(3):
                                try:
                                    await database_sync_to_async(News.objects.create)(
                                        meeting=meeting, keyword=keyword_instance, title=result[0]['title'][i], link=result[0]['link'][i]
                                    )
                                except IndexError:
                                    # 인덱스 오류가 발생하면 로그를 남기고 계속 진행
                                    print(f"IndexError: list index out of range for i={i}")
                            total.append(result)
                        meeting.meeting_text = meeting_text
                        await database_sync_to_async(meeting.save)()
                        self.total_data = total   
                        print('self.stt_running_send함수전', self.stt_running)
                        if not self.stt_running:
                            print('stt 종료됨')
                            break
                        start_time = time.time()

    async def receive(self, text_data):
        data = json.loads(text_data)
        
        if data['type'] == 'start_meeting':
            # "회의 시작" 메시지를 받으면 stt 함수 실행
            await self.stt()
        elif data['type'] == 'request_meeting_data':
            # 15초마다 total_data를 요청하는 메시지를 받으면 현재의 total 값을 보내줌
            print('self.stt_running', self.stt_running)
            print('self.total_data', self.total_data)
            if self.stt_running:
                self.send(text_data=json.dumps({
                    'meeting': 'total',
                    'meeting_data': self.total_data,
                }))
        elif data['type'] == 'finish_meeting':
            # "회의 종료" 메시지를 받으면 WebSocket을 종료
            self.stt_running = False
            print('self.stt_running False로 바뀜', self.stt_running)
            await self.close()

            
            
    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            token_obj = Token.objects.get(key=token)
            return token_obj.user
        except Token.DoesNotExist:
            return None


