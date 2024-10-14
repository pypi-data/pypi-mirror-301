from setuptools import setup, find_packages

setup(
    name='whassup-V11.1.2',  # 패키지 이름
    version='11.1.2',  # 패키지 버전
    packages=find_packages(include=['whassup', 'whassup.*']),  # 패키지 자동 검색
    install_requires=[  # 의존성 목록
        'Django>=3.0',
        'opencv-python',
        'numpy',
        'deepface',
        # 다른 의존성 추가
    ],
    entry_points={  # 실행 진입점 (선택 사항)
        'console_scripts': [
            'whatsup=manage:main',  # 명령어와 함수 연결
        ],
    },
    author='Your Name',  # 작성자
    author_email='your_email@example.com',  # 이메일
    description='A brief description of your project',  # 설명
    long_description=open('README.md', encoding='utf-8').read(),  # 긴 설명
    long_description_content_type='text/markdown',  # 설명 형식
    url='https://github.com/yourusername/whatsup',  # 프로젝트 URL
    classifiers=[  # 분류자
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Python 버전 요구 사항
)

