import cv2
import numpy as np
from deepface import DeepFace
import logging
import os
import csv
from django.conf import settings

logger = logging.getLogger(__name__)

def analyze_face_emotion(image):
    try:
        np_image = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
        
        result = DeepFace.analyze(np_image, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        
        recommendations = {
            'happy': '오늘 정말 기분이 좋아보이네요!',
            'sad': '힘내세요, 좋은 일이 있을 거예요.',
            'angry': '화가 나셨군요, 진정하세요.',
            'neutral': '평온해 보이네요.',
            'fear': '무서운 일이 있었나요? 괜찮아질 거예요.',
            'surprise': '놀란 일이 있었나 봐요!',
            'disgust': '불쾌한 일이 있었나요?'
        }
        
        message = recommendations.get(emotion, '감정을 인식할 수 없습니다.')
        
        return {
            'emotion': emotion,
            'message': message
        }
    except Exception as e:
        logger.error(f"얼굴 감정 분석 중 오류 발생: {str(e)}", exc_info=True)
        raise
    
def update_emotion_data(emotion, score):
    # CSV 파일 경로 설정
    csv_file_path = os.path.join(settings.BASE_DIR, 'emotion_data.csv')
    
    # CSV 파일이 존재하지 않으면 헤더를 포함하여 생성
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Emotion', 'Score'])
    
    # 데이터를 CSV 파일에 추가
    with open(csv_file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([emotion, score])
    
    logger.info(f"감정 데이터 업데이트: {emotion}, 점수: {score}")
    
    # 데이터 개수 확인
    with open(csv_file_path, 'r') as file:
        data_count = sum(1 for row in file) - 1  # 헤더 제외
    
    # 데이터가 1000개 이상 모이면 모델 재학습 함수 호출
    if data_count >= 1000:
        retrain_model(csv_file_path)

def retrain_model(data_file):
    logger.info("모델 재학습 시작")
    # TODO: 여기에 실제 모델 재학습 로직을 구현합니다.
    # 예: 데이터를 읽어와서 DeepFace 모델을 fine-tuning
    logger.info("모델 재학습 완료")

def retrain_model(data_file):
    logger.info("모델 재학습 시작")
    # TODO: 여기에 실제 모델 재학습 로직을 구현합니다.
    # 예: 데이터를 읽어와서 DeepFace 모델을 fine-tuning
    logger.info("모델 재학습 완료")