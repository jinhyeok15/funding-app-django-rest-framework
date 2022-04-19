# 구현하기

## 목록

* 환경 세팅하기
  1. 서버 환경 (stacks)
  2. 로컬 실행
  3. Swagger django 연동
  4. TestCase 설정
* API 구축
  1. apps
  2. models 설계
  3. 상품 등록
  4. 상품 수정
  5. 상품 삭제
  6. 상품 목록 조회

## 환경 세팅하기

### 1. 서버 환경 (stacks)

* Python 3.7
* Django 2.1.7
* DRF 3.11.0
* postgresql(RDS)
* Docker v18.09.2
* Docker Compose v1.23.2

서버 환경은 [realpython/dockerizing-django](https://github.com/realpython/dockerizing-django)를 기반으로 customizing하여 구축하였습니다.
env파일에서 RDS세팅 관련 보안 문제가 있어, settings 파일에서 중요 부분을 따로 json으로 저장하여, jwt를 받아 conf.ini에 저장하였습니다.
conf.ini파일은 aws S3에서 관리합니다.

### 2. 로컬 실행

S3 url에서 conf.ini 파일 다운로드. src/funding 디렉토리에 붙여넣기

다음 명령어 실행

``` shell
cd src
pip install -r requirements.txt
python manage.py runserver
```

### 3. Swagger django 연동

[참고](https://github.com/axnsan12/drf-yasg)

Connect

> 127.0.0.1:8000/swagger\
> 127.0.0.1:8000/redoc

### 4. TestCase 설정

> [django test](https://docs.djangoproject.com/en/4.0/topics/testing/overview/)\
> [drf test](https://www.django-rest-framework.org/api-guide/testing/)

```python manage.py test```

## API 구축

### 1. apps

앱은 유저 관련 info를 처리하는 profile과 펀딩 샵 부분을 담당하는 shop이 있습니다. 펀딩 샵과 다른 도메인 간의 재사용성을 고려하여, 일부 django 객체 및 components는 abstract 앱에서 관리합니다.
