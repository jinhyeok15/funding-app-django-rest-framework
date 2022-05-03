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
        self.message = "date 타입에 맞지 않습니다"
        super().__init__(self.message, {"date": value})


class CannotWriteError(DjangoValidationError):
    """
    Read-only-field cannot write
    """
    status = "CANNOT_WRITE"
    def __init__(self, code):
        self.message = "Read-only-field cannot write"
        super().__init__(self.message, code)


# user
class DoesNotExistedUserPocketError(DjangoValidationError):
    """
    유저가 지갑을 등록하지 않았습니다.
    """
    status = "DOES_NOT_EXIST_USER_POCKET"
    def __init__(self, user_id):
        self.message = "유저가 지갑을 등록하지 않았습니다."
        super().__init__(self.message, {
            "user_id": user_id
        })


# shop
class UserAlreadyParticipateError(DjangoValidationError):
    """
    유저가 이미 참여한 게시물입니다.
    """
    status = "USER_ALREADY_PARTICIPATE"
    def __init__(self, user_id, post_id):
        self.message = "유저가 이미 참여한 게시물입니다."
        super().__init__(self.message, {
            "user_id": user_id,
            "post_id": post_id
        })


class PostCannotParticipateError(DjangoValidationError):
    """
    게시물에 접근할 수 없어 참여할 수 없습니다.
    """
    status = "POST_CANNOT_PARTICIPATE"
    def __init__(self, post_id):
        self.message = "게시물에 접근할 수 없어 참여할 수 없습니다."
        super().__init__(self.message, {"post_id": post_id})


class PosterCannotParticipateError(DjangoValidationError):
    """
    게시자는 참여할 수 없습니다.
    """
    status = "POSTER_CANNOT_PARTICIPATE"
    def __init__(self, user_id):
        self.message = "게시자는 참여할 수 없습니다."
        super().__init__(self.message, {"poster": user_id})


class PostDoesNotExistError(DjangoValidationError):
    """
    게시물이 존재하지 않습니다.
    """
    status = "POST_DOES_NOT_EXIST"
    def __init__(self, post_id):
        self.message = "게시물이 존재하지 않습니다."
        super().__init__(self.message, {"post_id": post_id})


class UserCannotModifyPostError(DjangoValidationError):
    """
    게시물 수정 권한이 없습니다.
    """
    status = "USER_CANNOT_MODIFY_POST"
    def __init__(self, user_id, post_id):
        self.message = "게시물 수정 권한이 없습니다."
        super().__init__(self.message, {"user_id": user_id, "post_id": post_id})
