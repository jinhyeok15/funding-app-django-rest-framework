# 서비스 분석

## 서비스 개요 분석

* User type: 일반유저/게시자
* 유저는 상품을 1회까지만 펀딩할 수 있다.
* 유저는 결제할 수 있는 Pocket을 등록한 후 purchase할 수 있다.
* ShopPost에는 status=PURCHASE/DONATE/CANCEL/CLOSE 컬럼이 존재한다. PURCHASE는 펀딩이 성공적으로 진행되어 구매단계까지 진행된 상태이며, DONATE는 펀딩에 참여하였으나 마감일이 끝나지 않은 상태, CANCEL은 펀딩을 취소한 상태, CLOSE는 펀딩 목표 금액을 넘지 못하여 펀딩이 취소된 상태를 의미한다. 결제는 PURCHASE단계에서 진행되며, CANCEL이 되면 결제 내역이 환불된다.
* 펀딩 shop 도메인에서 결제부분을 따로 빼는 것을 고려하였으나, 기존 앱에서 펀딩 shop 도메인을 추가하는 것이라면 shop 내부에서 purchase 내역을 관리하는 것이 좋을 것으로 판단하였음
* ShopPurchaseLog에서 User, Item을 UniqueConstraint로 묶어서 관리해야 한다.(유저가 한개의 상품에 여러번 DONATE 불가능) 하지만 현재 Django 버전이 2.1.7로 UniqueConstraint는 공식문서에서 4.0 버전에서 다루는 것을 추천한다. 대안책으로 모델에서 post를 할 경우 get_or_create를 활용한다.
