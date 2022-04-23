from rest_framework.response import Response
from rest_framework import status
from typing import Optional


__all__ = [
        'HttpStatus',
        'InheritedResponse',
        ]


def _get_status_by_code(code):
    _status = vars(status)
    try:
        idx = list(_status.values()).index(code)
        return list(_status.keys())[idx]
    except ValueError as e:
        raise ValueError("존재하지 않는 코드입니다\n"+str(e))


class HttpStatus:
    """
    rest_framework status의 status code 기반으로 status와 code, custom message를 갖고 있는 object
    """
    def __init__(self, code, message=None, error=None, schema=None):
        self.code = code
        self.status = _get_status_by_code(code)
        self.message = message
        if error is not None:
            self.message = error.args[0] + "\n" + self.message if self.message is not None else error.args[0]
            self.errors = error.args[1]
        self.schema = schema


class InheritedResponse(Response):
    """
    import InheritedResponse as Response\n
    Response 객체를 받아서 data형식에 맞게 변환시켜 전달한다\n
    생성자 인자로는 data와 HttpStatus를 받는다. -> Response(data, HttpStatus(400))\n
    기존 Response 객체와 유사하게 사용하여도 된다. (추천 사항은 아님) -> Response(data={}, status=status.HTTP_200_OK)\n
    4xx 혹은 5xx status의 경우 data 대신 errors를 전달해야 한다.
    """
    def __init__(self, data=None, http: Optional[HttpStatus]=None, **kwargs):
        status_code = http.code
        
        if http is not None:
            if status.is_client_error(status_code) or status.is_server_error(status_code):
                data_format = {
                    "code": status_code,
                    "status": http.status,
                    "message": http.message,
                    "errors": http.errors
                }
            else:
                data_format = {
                    "code": status_code,
                    "status": http.status,
                    "message": http.message,
                    "data": data
                }

            super().__init__(
                data_format, status_code, **kwargs
            )
        else:
            super().__init__(data, **kwargs)
