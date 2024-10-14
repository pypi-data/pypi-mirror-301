import cv2
import numpy as np
import base64
import time
import os
import json
import logging
import pytz
from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.utils import timezone
import traceback
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from deepface import DeepFace
from .models import EmotionAnalysis
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from datetime import datetime, timedelta, time
from .weather_service import get_weather, convert_grid
from .face_recognition_service import analyze_face_emotion, update_emotion_data

logger = logging.getLogger(__name__)

SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/tasks.readonly'
]

def index(request):
    return render(request, 'whassup/index.html')

@csrf_exempt
def analyze_emotion(request):
    if request.method == 'POST':
        try:
            if 'image' not in request.FILES:
                raise ValueError("이미지 파일이 수신되지 않았습니다.")
            
            image = request.FILES['image']
            result = analyze_face_emotion(image)
            
            return JsonResponse(result)
        except Exception as e:
            logger.error(f"감정 분석 중 오류 발생: {str(e)}", exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=405)

@require_POST
@csrf_exempt
def submit_emotion(request):
    try:
        data = json.loads(request.body)
        emotion = data.get('emotion')
        score = data.get('score')
        
        if emotion and score:
            update_emotion_data(emotion, int(score))
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'error': '감정 또는 점수가 제공되지 않았습니다.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_POST
def logout_view(request):
    logout(request)
    return JsonResponse({'status': 'success'})

def google_calendar_init(request):
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
        scopes=SCOPES
    )
    flow.redirect_uri = request.build_absolute_uri('/google-calendar/callback/')
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    request.session['state'] = state
    return HttpResponseRedirect(authorization_url)

def google_calendar_callback(request):
    try:
        state = request.session['state']
        flow = Flow.from_client_secrets_file(
            settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
            scopes=SCOPES,
            state=state
        )
        flow.redirect_uri = request.build_absolute_uri('/google-calendar/callback/')
                
        flow.fetch_token(code=request.GET.get('code'))
        credentials = flow.credentials
        
        request.session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        return redirect('index')
    except Exception as e:
        error_message = f"An error occurred: {str(e)}\n\n{traceback.format_exc()}"
        return HttpResponse(error_message, status=500)
    
    service = build('calendar', 'v3', credentials=credentials)
    
    # 이번 달의 시작일과 종료일 계산
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1).isoformat() + 'Z'
    if now.month == 12:
        end_of_month = datetime(now.year + 1, 1, 1).isoformat() + 'Z'
    else:
        end_of_month = datetime(now.year, now.month + 1, 1).isoformat() + 'Z'
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_of_month,
        timeMax=end_of_month,
        maxResults=100,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    # 원시 데이터 로깅
    logger.info("Raw events data: %s", json.dumps(events, indent=2, ensure_ascii=False))

    simplified_events = []
    for event in events:
        simplified_event = {
            'summary': event['summary'],
            'start_date': '',
            'start_time': '',
            'end': event['end'].get('date') or event['end'].get('dateTime'),
        }
        
        start = event['start'].get('date') or event['start'].get('dateTime')
        
        # 날짜 형식 변환
        if 'T' in start:  # dateTime 형식인 경우
            start_dt = datetime.fromisoformat(start)
            end_dt = datetime.fromisoformat(simplified_event['end'])
            simplified_event['start_date'] = start_dt.strftime('%Y-%m-%d')
            simplified_event['start_time'] = start_dt.strftime('%H:%M')
            simplified_event['end'] = end_dt.strftime('%H:%M')
        else:  # date 형식인 경우
            simplified_event['start_date'] = start
            simplified_event['start_time'] = '종일'
            simplified_event['end'] = '종일'

        simplified_events.append(simplified_event)

    return render(request, 'whassup/calendar_events.html', {'events': simplified_events})

from django.http import JsonResponse, HttpResponseRedirect

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

def get_todays_events_and_tasks(request):
    try:
        if 'credentials' not in request.session:
            return JsonResponse({'redirect': '/google-calendar/init/'})
        
        credentials = Credentials(**request.session['credentials'])
        
        calendar_service = build('calendar', 'v3', credentials=credentials)
        tasks_service = build('tasks', 'v1', credentials=credentials)

        seoul_tz = pytz.timezone('Asia/Seoul')
        today = datetime.now(seoul_tz).date()
        start_of_day = datetime.combine(today, time.min).replace(tzinfo=seoul_tz)
        end_of_day = datetime.combine(today, time.max).replace(tzinfo=seoul_tz)

        # 이벤트 조회
        events_result = calendar_service.events().list(
            calendarId='primary',
            timeMin=start_of_day.isoformat(),
            timeMax=end_of_day.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        # 할 일 조회
        tasks_result = tasks_service.tasks().list(tasklist='@default').execute()
        tasks = tasks_result.get('items', [])

        items = []
        for event in events:
            items.append({
                'type': 'event',
                'summary': event['summary']
            })

        for task in tasks:
            if task['status'] != 'completed':
                items.append({
                    'type': 'task',
                    'summary': task['title']
                })

        return JsonResponse({'items': items})
    except Exception as e:
        print(f"Error in get_todays_events_and_tasks: {str(e)}")
        return JsonResponse({'error': '일정을 가져오는 중 오류가 발생했습니다.'}, status=500)

def logout(request):
    if 'credentials' in request.session:
        del request.session['credentials']
    return redirect('index') 

def clear_credentials(request):
    if 'credentials' in request.session:
        del request.session['credentials']
    return redirect('google_calendar_init')

#날씨 정보 조회
def weather_view(request):
    try:
        lat = float(request.GET.get('lat'))
        lon = float(request.GET.get('lon'))
        
        nx, ny = convert_grid(lat, lon)
        weather_info = get_weather(nx, ny)
        
        return JsonResponse({'weather': weather_info})
    except Exception as e:
        logger.error(f"날씨 정보 조회 중 오류 발생: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)