from rest_framework.serializers import ValidationError as SerializerValidationError
from django.core.exceptions import ValidationError as DjangoValidationError


class FinalDateValidationError(DjangoValidationError):
    """
    DateComponent 타입에는 yyyy-MM-dd 형식이 와야하며,
    현재 시각 기준으로 과거 date일 경우 final_date가 아니기 때문에 에러가 발생한다.
    """
    def __init__(self, value):
        self.message = f"date 타입에 맞지 않습니다: {value}"
        super().__init__(self.message)
