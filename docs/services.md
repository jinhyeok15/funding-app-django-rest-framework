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
  2. [POST shop/v1/post/](#2-post-shopv1post)
  3. [PATCH shop/v1/:post_id/](#3-patch-shoppostpost_id)
  4. [DELETE shop/v1/:post_id/](#4-delete-shopv1postpost_id)
  5. [GET shop/v1/:post_id](#5-get-shopv1postpost_id)
  6. [GET shop/v1/posts/](#6-get-shopv1posts)
  7. [POST shop/v1/<int:post_id>/participate/](#7-get-shopv1intpost_idwant_participate)
* 기타
  1. [Commit 관련 정리](#commit-관련-정리)
  2. [git commit convension](#git-commit-convention)
  3. [Apply swagger schema](#apply-swagger-schema)

## 서비스 분석

### 1. 개요

* User type: 일반유저/게시자

* 유저는 상품을 1회까지만 펀딩할 수 있다.

* 유저는 결제할 수 있는 Pocket을 등록한 후 purchase할 수 있다.

* ShopPost에는 status=SUCCESS/FUNDING/CLOSE/CANCEL 컬럼이 존재한다.
SUCCESS는 펀딩이 성공적으로 진행되어 상품 준비단계까지 진행된 상태이며,
FUNDING는 펀딩이 진행중인 상태,
CLOSE는 펀딩이 종료된 상태,
CANCEL는 펀딩 목표 금액을 넘지 못하여 펀딩이 취소된 상태를 의미한다.
결제는 DONATE단계에서 진행되며, CANCEL이 되면 결제 내역이 환불된다.

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

### 2. POST shop/v1/post/

# 펀딩 게시글 생성 API

* 개요

- 펀딩 게시글 생성 API

* 필수요건

1. request로 부터 header를 가져와서 User obj 가져오기

2. request.data 내부에서 Item 요소를 가져와 Item obj를 생성한다.

3. PostCreateSerializer를 생성하고, validation 진행 후 save한다.

4. Response 데이터로 post_id, user, item을 반환한다.

* 구현설명

게시자가 Item과 관련한 게시물을 작성한다는 점을 고려하여, Item과 Post 관련한 부분을 분리하였습니다. 
Funding shop 도메인에서는 Item이 핵심인 게시물이겠지만, 이후 커뮤니티로 발전할 경우와 같은 게시물의 확장성을 고려하였습니다. 
이렇게 될 경우, 단순히 게시물을 CREATE하는 API가 아닌, 게시자가 Item을 먼저 등록한 후 이를 게시한다는 논리 구조가 형성됩니다. 
이를 View에서 비즈니스 로직으로 구현하기 위해 두 개의 테이블에 접근하여 create하는 트랜잭션을 관리할 세션을 django.db.transaction 모듈을 통해 생성하였습니다.  

또한 request.data를 validation할 PostItemSerializer의 경우, AbstractPostItem model을 받아서 기존 모델(Item, ShopPost)와 형식이 맞지 않아 에러가 나는 부분을 해결했습니다.  

response에서는 client에서 사용할 게시물 id와 게시자 id, item id를 제공하여 client 측에서 접근할 수 있도록 하였습니다.

### 3. PATCH shop/v1/post/:post_id/

* 펀딩 상품 상세 수정 API

* 개요

- 게시물의 모든 내용이 수정 가능하나 '목표금액'은 수정이 불가능합니다.

* 필수요건

1. 게시자만 수정 가능합니다.
2. post_id를 통해 조회하는 post의 status 중 CLOSE는 포함하지 않는다.

### 4. DELETE shop/v1/post/:post_id/

* 펀딩 상품 상세 삭제 API

* 개요

- 게시물 중 펀딩 중인 상품은 참여자들이 모두 결제가 완료된 상태이기 때문에, 삭제가 불가능합니다. 삭제 요청만 가능합니다.

- 삭제 요청을 보내면 DB에 내역이 삭제됩니다.

* 필수요건

1. 게시자만 삭제 가능합니다.
2. post_id를 통해 조회하는 post의 status 중 CLOSE와 FUNDING은 포함하지 않는다.

### 5. GET shop/v1/post/:post_id/

* 펀딩 상품 상세 조회 API

* 개요

- 상품 상세 페이지를 가져옵니다.
- 제목, 게시자명, 총펀딩금액, 달성률, D-day(펀딩 종료일까지), 상품설명, 목표금액 및 참여자 수가 포함되어야 합니다.

* 필수요건

1. post_id를 통해 조회하는 post의 status 중 CLOSE는 포함하지 않는다.
2. 참여자 수를 계산해야 한다.

### 6. GET shop/v1/posts/

* 펀딩 상품 전체 조회 API

* 개요

- 제목, 게시자명, 총펀딩금액, 달성률 및 D-day(펀딩 종료일까지) 가 포함되어야 합니다.

- 상품을 검색하고 정렬합니다. 정렬은 생성일, 총펀딩금액별 정렬이 가능합니다.

* 필수요건

1. 조회는 10개씩 가능 limit=10, offset=n-1(nth page)
2. 상품 리스트 API 에 ?search=취미 조회 시 ,제목에  ‘내 취미 만들..’  ‘취미를 위한 ..’ 등 검색한 문자 포함된 상품 리스트만 조회
3. 생성일기준의 경우 인덱싱으로 조회 cache에서 가져온 object에서 그대로 pagination
4. 총 펀딩금액 기준으로 정렬을 할 경우에는 serializer에서 sorting 해야함
5. search 쿼리의 경우, 추후에 AWS ElasticSearch를 활용한다. 참조: http://labs.brandi.co.kr/2021/07/08/leekh.html

### 7. GET shop/v1/<int:post_id>/want_participate/

* 펀딩 상품 참여 가능 여부 체크 API

* 개요

- 펀딩 참여하기 버튼을 눌렀을 때, 상품 결제 창으로 옮겨진다.

- 결제 창으로 옮겨지기 전 해당 API를 통해 유저의 결제 상태를 체크한다.

* 필수요건

1. 유저 지갑 개설 여부 조회(is_active) 후, 개설이 되어 있을 경우 결제 진행.

2. 유저가 이미 참여를 한 경우 400 ValidationError

### 8. POST shop/v1/<int:post_id>/participate/

* 펀딩 상품 참여 등록 API

* 개요

- 유저가 결제를 성공할 경우에, 결제 내역을 기록하고, 유저 참여 여부를 등록한다.

* 필수요건

1. 유저가 이미 참여를 한 경우 400 ValidationError
2. 유저가 아닌 게시자의 경우 참여 불가
3. 결제 내역 기록, 유저 참여 여부 등록 transaction 구성

## 기타

### Commit 관련 정리

* [DEBUG] 디버그
* [API] API 개발
* [REFAC] 리팩토링
* [ENV] 환경 설정
* [DOC] 문서 관련 정리
* [TEST] 테스트

### git commit convention

[https://www.conventionalcommits.org/en/v1.0.0/](https://www.conventionalcommits.org/en/v1.0.0/)

### Apply swagger schema

[https://drf-yasg.readthedocs.io/en/stable/custom_spec.html](https://drf-yasg.readthedocs.io/en/stable/custom_spec.html)
