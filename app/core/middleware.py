import uuid
from contextvars import ContextVar

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.auth.security import verify_token
from app.core.constants import RATE_LIMIT_OTHER, RATE_LIMIT_POST, WINDOW

transaction_id_var = ContextVar("transaction_id", default=None)


def get_transaction_id():
    return transaction_id_var.get() or "no-transaction"


def set_transaction_id(transaction_id=None):
    if transaction_id is None:
        transaction_id = str(uuid.uuid4())
    transaction_id_var.set(transaction_id)
    return transaction_id


class TransactionIdMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        set_transaction_id(request.headers.get("X-Transaction-ID", None))

        response = await call_next(request)

        response.headers["X-Transaction-ID"] = get_transaction_id()
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        redis = request.app.state.redis
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if token:
            user_payload = verify_token(token)
            if not user_payload:
                return await call_next(request)
            rate_limit_identifier = user_payload.get("id")
        else:
            rate_limit_identifier = request.client.host
        RATE_LIMIT = RATE_LIMIT_POST if request.method == "POST" else RATE_LIMIT_OTHER
        redis_key = f"ratelimit:{rate_limit_identifier}"
        current_count = await redis.get(redis_key)
        if current_count is None:
            await redis.set(redis_key, 1, ex=WINDOW)
        elif int(current_count) < RATE_LIMIT:
            await redis.incr(redis_key)
        else:
            ttl = await redis.ttl(redis_key)
            return JSONResponse(
                status_code=429,
                content={"error": f"Rate limit exceeded, retry in {ttl} seconds"},
            )
        return await call_next(request)
