# 펀딩 앱 서버 프로젝트

## Docs

### [API 문서](docs/services.md)

### [Work Logs](docs/work.md)

## 활용 기술

### Language

* python 3.7

### Framework

* django
* django_restframework(DRF)

### Library

* PyJWT
* drf-yasg

### DB

* postgresql(RDS)

### Server

* (web) Nginx
* Docker
* (cache) redis

서버 환경은 [realpython/dockerizing-django](https://github.com/realpython/dockerizing-django)를 기반으로 customizing하여 구축하였습니다.
env파일에서 RDS세팅 관련 보안 문제가 있어, settings 파일에서 중요 부분을 따로 json으로 저장하여, jwt를 받아 conf.ini에 저장하였습니다.
conf.ini파일은 aws S3에서 관리합니다.

### Swagger django 연동

[참고](https://github.com/axnsan12/drf-yasg)

Connect

> 127.0.0.1:8000/swagger\
> 127.0.0.1:8000/redoc

### TestCase 설정

> [django test](https://docs.djangoproject.com/en/4.0/topics/testing/overview/)\
> [drf test](https://www.django-rest-framework.org/api-guide/testing/)

```python manage.py test```

## 주요 개발 부분
* View에 세부적인 비즈니스 로직은 Mixin에서 구현하도록 하여 View단에서는 Response 예외처리만 담당하도록 하였음.

* 모델 구조 재사용성을 위한 AbstractModel 활용

* 유저 토큰 기반 인증 구현

* 주석, 설명 상세화, swagger 기반 문서 Schema 작성 (Customizing)

* unittest 기반 API 개발

* JWT로 settings.py 보안 부분 token화 하여 ini파일로 관리.

* redis로 게시물 조회 부분 캐싱 -> 조회 속도 개선

* 데이터베이스 트랜잭션 처리

* exception 기반 view 로직 구성
  
## 서비스 관련 구현 사항

* User type: 일반유저/게시자 각각의 고유 권한이 있습니다. ->
  일반유저는 참여만 가능 / 게시자는 작성만 가능하고 참여는 불가

* 유저는 상품을 1회까지만 펀딩할 수 있습니다. UserAlreadyParticipateError raise

* 유저는 결제할 수 있는 Pocket을 등록한 후 purchase할 수 있습니다.

* ShopPost에는 status=SUCCESS/FUNDING/CLOSE/CANCEL 컬럼이 존재합니다.
SUCCESS는 펀딩이 성공적으로 진행되어 상품 준비단계까지 진행된 상태이며,
FUNDING는 펀딩이 진행중인 상태,
CLOSE는 펀딩이 종료된 상태,
CANCEL는 펀딩 목표 금액을 넘지 못하여 펀딩이 취소된 상태를 의미합니다.
결제는 DONATE단계에서 진행되며, CANCEL이 되면 결제 내역이 환불됩니다.

* 펀딩 shop 도메인에서 결제부분을 따로 빼는 것을 고려하였으나, 기존 앱에서 펀딩 shop 도메인을 추가하는 것이라면 shop 내부에서 purchase 내역을 관리하는 것이 좋을 것으로 판단하였습니다.

* 앱은 유저 관련 info를 처리하는 user 펀딩 샵 부분을 담당하는 shop이 있습니다. 펀딩 샵과 다른 도메인 간의 재사용성을 고려하여, 일부 django 객체 및 components는 core 앱에서 관리합니다.

* 상품 상세 페이지에서 총펀딩금액, 달성률, D-day, 참여자 수의 경우, serializer에서 SerializerMethodField를 사용하였습니다.
이 때, 조회 API 요청 각각마다 db 쿼리를 요청해야하므로 속도 저하 문제가 발생할 수 있기에, redis로 shop 메인 posts에 대해 cache처리를 하였습니다 => 기존 300ms에서 60ms로 속도 개선이 이루어졌습니다.

* 검색 기능에서는 keyword로 시작하는 post 전체를 조회합니다. 정렬은 생성일 순과 총 펀딩액 순이 있는데, ux관점에서 총 펀딩액 순을 default로 지정하는 것이 좋을 것으로 판단하였습니다. 정렬 부분은 db에서가 아닌 어플리케이션 쪽에서 구현하였지만 serializer쪽에서 post관련한 처리가 많아짐에 따라, post_figure 테이블을 추가하여, db쪽에서 sorting하는 것을 고려하고 있습니다.

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
