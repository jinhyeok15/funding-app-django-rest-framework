# API 문서
  1. [POST account/signup/](#1-post-accountsignup)
  2. [POST shop/v1/post/](#2-post-shopv1post)
  3. [PATCH shop/v1/post/:post_id/](#3-patch-shoppostpost_id)
  4. [DELETE shop/v1/post/:post_id/](#4-delete-shopv1postpost_id)
  5. [GET shop/v1/post/:post_id](#5-get-shopv1postpost_id)
  6. [GET shop/v1/posts/](#6-get-shopv1posts)
  7. [GET shop/v1/<int:post_id>/want_participate/](#7-get-shopv1intpost_idwant_participate)
  8. [POST shop/v1/<int:post_id>/participate/](#8-post-shopv1intpost_idparticipate)

## 1. POST account/signup

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

## 2. POST shop/v1/post/

* 펀딩 게시글 생성 API

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

## 3. PATCH shop/v1/post/:post_id/

* 펀딩 상품 상세 수정 API

* 개요

- 게시물의 모든 내용이 수정 가능하나 '목표금액'은 수정이 불가능합니다.

* 필수요건

1. 게시자만 수정 가능합니다.
2. post_id를 통해 조회하는 post의 status 중 CLOSE는 포함하지 않는다.

## 4. DELETE shop/v1/post/:post_id/

* 펀딩 상품 상세 삭제 API

* 개요

- 게시물 중 펀딩 중인 상품은 참여자들이 모두 결제가 완료된 상태이기 때문에, 삭제가 불가능합니다. 삭제 요청만 가능합니다.

- 삭제 요청을 보내면 DB에 내역이 삭제됩니다.

* 필수요건

1. 게시자만 삭제 가능합니다.
2. post_id를 통해 조회하는 post의 status 중 CLOSE와 FUNDING은 포함하지 않는다.

## 5. GET shop/v1/post/:post_id/

* 펀딩 상품 상세 조회 API

* 개요

- 상품 상세 페이지를 가져옵니다.
- 제목, 게시자명, 총펀딩금액, 달성률, D-day(펀딩 종료일까지), 상품설명, 목표금액 및 참여자 수가 포함되어야 합니다.

* 필수요건

1. post_id를 통해 조회하는 post의 status 중 CLOSE는 포함하지 않는다.
2. 참여자 수를 계산해야 한다.

## 6. GET shop/v1/posts/

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

## 7. GET shop/v1/<int:post_id>/want_participate/

* 펀딩 상품 참여 가능 여부 체크 API

* 개요

- 펀딩 참여하기 버튼을 눌렀을 때, 상품 결제 창으로 옮겨진다.

- 결제 창으로 옮겨지기 전 해당 API를 통해 유저의 결제 상태를 체크한다.

* 필수요건

1. 유저 지갑 개설 여부 조회(is_active) 후, 개설이 되어 있을 경우 결제 진행.

2. 유저가 이미 참여를 한 경우 400 ValidationError

## 8. POST shop/v1/<int:post_id>/participate/

* 펀딩 상품 참여 등록 API

* 개요

- 유저가 결제를 성공할 경우에, 결제 내역을 기록하고, 유저 참여 여부를 등록한다.

* 필수요건

1. 유저가 이미 참여를 한 경우 400 ValidationError
2. 유저가 아닌 게시자의 경우 참여 불가
3. 결제 내역 기록, 유저 참여 여부 등록 transaction 구성
