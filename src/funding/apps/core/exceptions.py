from django.core.exceptions import ValidationError as DjangoValidationError


class SerializerValidationError(DjangoValidationError):
    """
    DjangoValidationError를 기반으로 response를 구현하였기 때문에
    SerializerValidationError 구조도 DjangoValidationError를 따르게 한다
    """
    def __init__(self, message=None, code=None, params=None):
        self.message = message
        self.code = code
        self.params = params
        super().__init__(self.message, code=self.code, params=self.params)


class DoesNotIncludeStatusError(KeyError):
    def __init__(self):
        self.message = "Does not include status"
        super().__init__(self.message)


class FinalDateValidationError(DjangoValidationError):
    """
    DateComponent 타입에는 yyyy-MM-dd 형식이 와야하며,
    현재 시각 기준으로 과거 date일 경우 final_date가 아니기 때문에 에러가 발생한다.
    """
    message = "date 타입에 맞지 않습니다"
    code = "NOT_VALID_DATE_TYPE"

    def __init__(self, value):
        self.params = {"date": value}
        super().__init__(self.message, code=self.code, params=self.params)


class CannotWriteError(DjangoValidationError):
    """
    Read-only-field cannot write
    """
    message = "Read-only-field cannot write"
    code = "CANNOT_WRITE"

    def __init__(self, params):
        self.params = params
        super().__init__(self.message, code=self.code, params=params)


class UnsetPaginationError(DjangoValidationError):
    """
    Pagination 쿼리가 없습니다
    """
    message = "Pagination 쿼리가 없습니다"
    code = "UNSET_PAGINATION"

    def __init__(self):
        super().__init__(self.message, code=self.code)


class PageBoundException(DjangoValidationError):
    """
    페이지 범위를 벗어났습니다
    """
    message = "페이지 범위를 벗어났습니다"
    code = "PAGE_OUT_OF_BOUND"

    def __init__(self, max_page):
        self.params = {"max_page": max_page}
        super().__init__(self.message, code=self.code, params=self.params)


class NotFoundRequiredParameterError(DjangoValidationError):
    """
    필수 Request parameter가 존재하지 않습니다
    """
    message = "필수 Request parameter가 존재하지 않습니다"
    code = "NOT_FOUND_REQUIRED_PARAMETER"

    def __init__(self, key):
        self.params = {"required": key}
        super().__init__(self.message, code=self.code, params=self.params)
    

class TargetAmountBoundException(DjangoValidationError):
    """
    목표 금액은 10000원 이상만 등록 가능합니다
    """
    message = "목표 금액은 10000원 이상만 등록 가능합니다"
    code = "TARGET_AMOUNT_OUT_OF_BOUND"

    def __init__(self, value):
        self.params = {"target_amount": value}
        super().__init__(self.message, code=self.code, params=self.params)


# user
class DoesNotExistedUserPocketError(DjangoValidationError):
    """
    유저가 지갑을 등록하지 않았습니다.
    """
    message = "유저가 지갑을 등록하지 않았습니다."
    code="DOES_NOT_EXIST_USER_POCKET"

    def __init__(self, user_id):
        self.params={
            "user_id": user_id
        }
        super().__init__(self.message, code=self.code, params=self.params)


# shop
class UserAlreadyParticipateError(DjangoValidationError):
    """
    유저가 이미 참여한 게시물입니다.
    """
    message = "유저가 이미 참여한 게시물입니다."
    code="USER_ALREADY_PARTICIPATE"

    def __init__(self, user_id, post_id):
        self.params = {
            "user_id": user_id,
            "post_id": post_id
        }
        super().__init__(self.message, code=self.code, params=self.params)


class PostCannotParticipateError(DjangoValidationError):
    """
    게시물에 접근할 수 없어 참여할 수 없습니다.
    """
    message = "게시물에 접근할 수 없어 참여할 수 없습니다."
    code = "POST_CANNOT_PARTICIPATE"

    def __init__(self, post_id):
        self.params = {"post_id": post_id}
        super().__init__(self.message, code=self.code, params=self.params)


class PosterCannotParticipateError(DjangoValidationError):
    """
    게시자는 참여할 수 없습니다.
    """
    message = "게시자는 참여할 수 없습니다."
    code = "POSTER_CANNOT_PARTICIPATE"

    def __init__(self, user_id):
        self.params = {"poster": user_id}
        super().__init__(self.message, code=self.code, params=self.params)


class PostDoesNotExistError(DjangoValidationError):
    """
    게시물이 존재하지 않습니다.
    """
    message = "게시물이 존재하지 않습니다."
    code="POST_DOES_NOT_EXIST"

    def __init__(self, post_id):
        self.params = {"post_id": post_id}
        super().__init__(self.message, code=self.code, params=self.params)


class UserCannotModifyPostError(DjangoValidationError):
    """
    게시물 수정 권한이 없습니다.
    """
    message = "게시물 수정 권한이 없습니다."
    code = "USER_CANNOT_MODIFY_POST"

    def __init__(self, user_id, post_id):
        self.params = {"user_id": user_id, "post_id": post_id}
        super().__init__(self.message, code=self.code, params=self.params)
