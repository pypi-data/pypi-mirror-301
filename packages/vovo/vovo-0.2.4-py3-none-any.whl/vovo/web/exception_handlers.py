from fastapi import Request
from fastapi.responses import JSONResponse

from vovo.core.api import APIResponse, APIError
from vovo.exceptions import VovoBusinessException


async def business_exception_handler(request: Request, exc: VovoBusinessException):
    """业务异常处理"""

    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(success=False, error=APIError(error_code=exc.code, message=exc.detail),
                            data=None).model_dump(),
    )