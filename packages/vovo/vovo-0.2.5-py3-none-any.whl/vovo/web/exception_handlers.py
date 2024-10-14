from fastapi import Request
from fastapi.responses import JSONResponse

from vovo.core.api import APIResponse, APIError
from vovo.exceptions import VovoBusinessException


async def business_exception_handler(request: Request, exc: Exception):
    """业务异常处理"""

    if isinstance(exc, VovoBusinessException):
        return JSONResponse(
            status_code=exc.status_code,
            content=APIResponse(success=False, error=APIError(error_code=exc.code, message=exc.detail),
                                data=None).model_dump())
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "An unexpected error occurred"}
        )