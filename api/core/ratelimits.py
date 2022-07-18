from slowapi import Limiter
from starlette.requests import Request
from common.config import config
import secrets


def handle_ratelimits(request: Request) -> str:
    if "Authorization" in request.headers:
        if request.headers["Authorization"] in config.get("no_ratelimit_keys", []):
            return secrets.token_urlsafe(32)
    else:
        if "X_FORWARDED_FOR" in request.headers:
            r = request.headers["X_FORWARDED_FOR"]
            return r
        else:
            return request.client.host or "127.0.0.1"


limiter = Limiter(
    key_func=handle_ratelimits,
    headers_enabled=True,
    storage_uri=config["redis_urls"]["ratelimits"],
)
