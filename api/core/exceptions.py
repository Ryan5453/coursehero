from fastapi import Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from starlette.exceptions import HTTPException

from api.core.ratelimits import limiter
from api.server import app


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request, exception: HTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={"message": exception.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exception: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "message": "One or more parameters are invalid. Please check the documentation for more information."
        },
    )


@app.exception_handler(RateLimitExceeded)
def ratelimit_handler(request: Request, exception: RateLimitExceeded) -> Response:
    response = JSONResponse(
        {
            "message": f"Slow down! You've exceeded your ratelimits. Please check the headers for ratelimit information."
        },
        status_code=429,
    )
    response = limiter._inject_headers(response, request.state.view_rate_limit)
    return response


@app.exception_handler(Exception)
async def main_exception_handler(request: Request, exception: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "message": "Something went wrong. This is on our end and should hopefully be fixed soon."
        },
    )
