# 구현하기

## 목록

* 서비스 분석
  1. 개요
  2. 요구사항
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

## 개요

* User type: 일반유저/게시자
* 유저는 상품을 1회까지만 펀딩할 수 있다.
* 유저는 결제할 수 있는 Pocket을 등록한 후 purchase할 수 있다.
* ShopPost에는 status=SUCCESS/DONATE/CANCEL/CLOSE 컬럼이 존재한다. PURCHASE는 펀딩이 성공적으로 진행되어 상품 준비단계까지 진행된 상태이며, DONATE는 펀딩에 참여하였으나 마감일이 끝나지 않은 상태, CANCEL은 펀딩을 취소한 상태, CLOSE는 펀딩 목표 금액을 넘지 못하여 펀딩이 취소된 상태를 의미한다. 결제는 DONATE단계에서 진행되며, CANCEL이 되면 결제 내역이 환불된다.
* 펀딩 shop 도메인에서 결제부분을 따로 빼는 것을 고려하였으나, 기존 앱에서 펀딩 shop 도메인을 추가하는 것이라면 shop 내부에서 purchase 내역을 관리하는 것이 좋을 것으로 판단하였음
* ShopPurchaseLog에서 User, Item을 UniqueConstraint로 묶어서 관리해야 한다.(유저가 한개의 상품에 여러번 DONATE 불가능) 하지만 현재 Django 버전이 2.1.7로 UniqueConstraint는 공식문서에서 4.0 버전에서 다루는 것을 추천한다. 대안책으로 모델에서 post를 할 경우 get_or_create를 활용한다.
* 앱은 유저 관련 info를 처리하는 profile과 펀딩 샵 부분을 담당하는 shop이 있습니다. 펀딩 샵과 다른 도메인 간의 재사용성을 고려하여, 일부 django 객체 및 components는 abstract 앱에서 관리합니다.

### abstract model

```python
# apps/abstract/models

from tkinter import CASCADE
from django.db import models
from funding.apps.user.models import User


class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        abstract = True


class PurchaseInterface(models.Model):
    user: models.ForeignKey
    production: models.ForeignKey

    class Meta:
        abstract = True

```

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

### 2. 로그인 구현

[참고: How to Implement Token Authentication using Django REST Framework](https://simpleisbetterthancomplex.com/tutorial/2018/11/22/how-to-implement-token-authentication-using-django-rest-framework.html)
