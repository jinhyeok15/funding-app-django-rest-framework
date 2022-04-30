from rest_framework.serializers import ValidationError as SerializerValidationError
from django.core.exceptions import ValidationError as DjangoValidationError


class DoesNotIncludeStatusError(KeyError):
    def __init__(self):
        self.message = "Does not include status"
        super().__init__(self.message)


class FinalDateValidationError(DjangoValidationError):
    """
    DateComponent 타입에는 yyyy-MM-dd 형식이 와야하며,
    현재 시각 기준으로 과거 date일 경우 final_date가 아니기 때문에 에러가 발생한다.
    """
    status = "NOT_VALID_DATE_TYPE"
    def __init__(self, value):
        self.message = f"date 타입에 맞지 않습니다: {value}"
        super().__init__(self.message)


# user
class DoesNotExistedUserPocketError(DjangoValidationError):
    status = "DOES_NOT_EXIST_USER_POCKET"
    def __init__(self, user_id):
        self.message = "유저가 지갑을 등록하지 않았습니다."
        super().__init__(self.message, {
            "user_id": user_id
        })


#shop
class UserAlreadyParticipateError(DjangoValidationError):
    status = "USER_ALREADY_PARTICIPATE"
    def __init__(self, user_id, post_id):
        self.message = "유저가 이미 참여한 게시물입니다."
        super().__init__(self.message, {
            "user_id": user_id,
            "post_id": post_id
        })
