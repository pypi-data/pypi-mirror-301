from typing import Any


class VovoException(Exception):
    def __init__(self, code: str, detail: str):
        self.code = code
        self.details = detail


class VovoBusinessException(VovoException):
    """Vovo 业务异常的基类"""

    def __init__(self, detail: str, code: str = "BusinessError", status_code: int = 400):
        self.detail = detail
        self.code = code
        self.status_code = status_code


class VovoHttpException(VovoException):
    """Vovo HTTP 异常的基类"""


class ParserException(ValueError, VovoException):
    """解析器应引发异常以表示解析错误"""

    def __init__(self, error: Any):
        super(ParserException, self).__init__(error)
