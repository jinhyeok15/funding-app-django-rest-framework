# 원티드러닝 프리온보딩 백엔드 2차 코스 지원 과제

## Stack
* Python 3.7
* Django 2.1.7
* DRF 3.11.0
* postgresql(RDS)
* Docker v18.09.2
* Docker Compose v1.23.2

## Work Logs
[click here](doc/work.md)

## Settings
전달드린 S3 url에서 conf.ini 파일 다운로드. src/funding 디렉토리에 붙여넣기

### Local Test
다음 명령어 실행
```
cd src
pip install -r requirements.txt
python manage.py runserver
```

## Swagger 문서 자동화
[참고](https://github.com/axnsan12/drf-yasg)

### Connect
127.0.0.1:8000/swagger
127.0.0.1:8000/redoc

## TestCase
[django test](https://docs.djangoproject.com/en/4.0/topics/testing/overview/)
[drf test](https://www.django-rest-framework.org/api-guide/testing/)

```python manage.py test```

## Commit 관련 정리
* [DBG] 디버그
* [API] API 개발
* [RFC] 리팩토링
* [ENV] 환경 설정
* [DOC] 문서 관련 정리
