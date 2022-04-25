# 구현하기

## 목록

* 서비스 분석
  1. 개요
  2. ~요구사항 => APIS와 병합~
* 환경 세팅하기
  1. 서버 환경 (stacks)
  2. 로컬 실행
  3. Swagger django 연동
  4. TestCase 설정
* API 구축
  1. [POST account/signup/](#1-post-accountsignup)
  2. [POST shop/post/](#2-post-shoppost-v100)
  3. [PATCH shop/post/:post_id/](#3-patch-shoppostpost_id)
  4. [DELETE shop/post/:post_id/](#4-delete-shoppostpost_id)
  5. [GET shop/post/:post_id](#5-get-shoppostpost_id)
  6. [GET shop/posts/](#6-get-shopposts)

## 서비스 분석

### 1. 개요

* User type: 일반유저/게시자

* 유저는 상품을 1회까지만 펀딩할 수 있다.

* 유저는 결제할 수 있는 Pocket을 등록한 후 purchase할 수 있다.

* ShopPost에는 status=SUCCESS/DONATE/CANCEL/CLOSE 컬럼이 존재한다. PURCHASE는 펀딩이 성공적으로 진행되어 상품 준비단계까지 진행된 상태이며, DONATE는 펀딩에 참여하였으나 마감일이 끝나지 않은 상태, CANCEL은 펀딩을 취소한 상태, CLOSE는 펀딩 목표 금액을 넘지 못하여 펀딩이 취소된 상태를 의미한다. 결제는 DONATE단계에서 진행되며, CANCEL이 되면 결제 내역이 환불된다.

* 펀딩 shop 도메인에서 결제부분을 따로 빼는 것을 고려하였으나, 기존 앱에서 펀딩 shop 도메인을 추가하는 것이라면 shop 내부에서 purchase 내역을 관리하는 것이 좋을 것으로 판단하였음

* ShopPurchaseLog에서 User, Item을 UniqueConstraint로 묶어서 관리해야 한다.(유저가 한개의 상품에 여러번 DONATE 불가능) 하지만 현재 Django 버전이 2.1.7로 UniqueConstraint는 공식문서에서 4.0 버전에서 다루는 것을 추천한다. 대안책으로 모델에서 post를 할 경우 get_or_create를 활용한다.

* 앱은 유저 관련 info를 처리하는 profile과 펀딩 샵 부분을 담당하는 shop이 있습니다. 펀딩 샵과 다른 도메인 간의 재사용성을 고려하여, 일부 django 객체 및 components는 abstract 앱에서 관리합니다.

> abstract model

```python
# apps/abstract/models

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


class AbstractPostItem(models.Model):
    title: models.CharField
    poster_name: models.CharField
    final_date: models.CharField
    content: models.TextField
    target_amount: models.IntegerField
    price: models.IntegerField
```

## 2. 환경 세팅하기

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

## 3. API 구축

### 1. POST account/signup

[참고: How to Implement Token Authentication using Django REST Framework](https://simpleisbetterthancomplex.com/tutorial/2018/11/22/how-to-implement-token-authentication-using-django-rest-framework.html)

* RequestBody(required)

```json
{
    "username": "진혁이",
    "email": "fhfhfh@email.com",
    "password": "12345678"
}
```

* Response(200)
* Response(400)

### 2. POST shop/post/ v1.0.0

* Header(required)

```json
{"Authorization": "Token {your token}"}
```

* RequestBody(required)

```json
{
    "title": "안녕하세요",
    "poster_name": "제 이름은",
    "content": "djfjfjfjfjfjd",
    "target_amount": 10000000,
    "final_date": "2022-04-22",
    "price": 500000
}
```

* Response(200)

```json
{
    "code": 201,
    "status": "HTTP_201_CREATED",
    "message": "생성완료",
    "data": {
        "id": 23,
        "item": {
            "id": 36,
            "tag": null,
            "price": 15000,
            "target_amount": 1000000,
            "updated_at": "2022-04-25T19:06:34.218149+09:00"
        },
        "poster": {
            "id": 2,
            "username": "jinhyeok",
            "email": "jinhyeok@email.com"
        },
        "title": "운동화?슬리퍼?고정관념x혁신적인 창조력넘치는 MANEUL마누어 스니커즈",
        "content": "운동화+슬리퍼=MANEUL 마누어 바캉스 스니커즈\nMANEUL 마누어 신어본 사람이 모두 놀라는 마법같은 신발\n고정관념 파괴하고 창조력 넘치는  관심 백퍼 인기 신발을 찾는다면 펀딩하세요.\n새로운 도전의 시작에 함께 해주셔서 감사합니다.",
        "created_at": "2022-04-25T19:06:34.273885+09:00",
        "updated_at": "2022-04-25T19:06:34.273947+09:00",
        "poster_name": "dkfk",
        "final_date": "2022-04-30",
        "status": "DONATE"
    }
}
```

* Response(400)

```json
{
    "code": 400,
    "status": "HTTP_400_BAD_REQUEST",
    "message": "Not valid serializer ShopPostItemRequestSerializer",
    "errors": {
        "poster_name": [
            "This field may not be null."
        ]
    }
}
```

* Description

게시자가 Item과 관련한 게시물을 작성한다는 점을 고려하여, Item과 Post 관련한 부분을 분리하였습니다. Funding shop 도메인에서는 Item이 핵심인 게시물이겠지만, 이후 커뮤니티로 발전할 경우와 같은 게시물의 확장성을 고려하였습니다. 이렇게 될 경우, 단순히 게시물을 CREATE하는 API가 아닌, 게시자가 Item을 먼저 등록한 후 이를 게시한다는 논리 구조가 형성됩니다. 이를 View에서 비즈니스 로직으로 구현하기 위해 두 개의 테이블에 접근하여 create하는 트랜잭션을 관리할 세션을 django.db.transaction 모듈을 통해 생성하였습니다.  

또한 request.data를 validation할 PostItemSerializer의 경우, AbstractPostItem model을 받아서 기존 모델(Item, ShopPost)와 형식이 맞지 않아 에러가 나는 부분을 해결했습니다.  

response에서는 client에서 사용할 게시물 id와 게시자 id, item id를 제공하여 client 측에서 접근할 수 있도록 하였습니다.

### 3. PATCH shop/post/:post_id/

### 4. DELETE shop/post/:post_id/

### 5. GET shop/post/:post_id/

### 6. GET shop/posts/
