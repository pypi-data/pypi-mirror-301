from setuptools import setup, find_packages

setup(
    name='whassup-V12.1.2',  # 패키지 이름
    version='12.1.2',  # 패키지 버전
    packages=find_packages(include=['whassup', 'whassup.*']),  # 패키지 자동 검색
    install_requires=[  # 의존성 목록
        'Django>=3.0,<4.0',  # Django 4.0 이상 버전과의 호환성 문제 방지
        'opencv-python>=4.5.0',  # 특정 버전 이상으로 설정
        'numpy>=1.19.0,<2.0.0',  # numpy 버전 조정
        'deepface==0.093',  # deepface의 경우 버전 명시 필요 시 추가
        # 다른 의존성 추가
    ],
    entry_points={  # 실행 진입점 (선택 사항)
        'console_scripts': [
            'whatsup=manage:main',  # 명령어와 함수 연결
        ],
    },
    author='Blacknight',  # 작성자
    author_email='sunugahn@gmail.com',  # 이메일
    description='to development a face and emotion recognition system',  # 설명
    long_description=open('README.md', encoding='utf-8').read(),  # 긴 설명
    long_description_content_type='text/markdown',  # 설명 형식
    url='https://github.com/Blacknight-dev/whatsup',  # 프로젝트 URL
    classifiers=[  # 분류자
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',  # Python 버전 요구 사항
)
