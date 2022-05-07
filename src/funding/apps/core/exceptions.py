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


class UnsetPaginationError(DjangoValidationError):
    """
    Pagination 쿼리가 없습니다
    """
    status = "UNSET_PAGINATION"
    def __init__(self):
        self.message = "Pagination 쿼리가 없습니다"
        super().__init__(self.message)


class PageBoundException(DjangoValidationError):
    """
    페이지 범위를 벗어났습니다
    """
    status = "PAGE_OUT_OF_BOUND"
    def __init__(self, max_page):
        self.message = "페이지 범위를 벗어났습니다"
        super().__init__(self.message, {"max_page": max_page})


class NotFoundRequiredParameterError(DjangoValidationError):
    """
    필수 Request parameter가 존재하지 않습니다
    """
    status = "NOT_FOUND_REQUIRED_PARAMETER"
    def __init__(self, key):
        self.message = "필수 Request parameter가 존재하지 않습니다"
        super().__init__(self.message, {"required": key})


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
