from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.auth.utils import verify_session_token
from app.config import Config


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if Config.SESSION_COOKIE_NAME is None:
            raise ValueError("SESSION_COOKIE_NAME is not set in the environment variables.")
        token = request.cookies.get(Config.SESSION_COOKIE_NAME,"")
        user = None
        if token:
            try:
                session = verify_session_token(token)
                db = request.app.state.database
                user = await db["users"].find_one({"email":session.get("email")})
                if not user:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session token")
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session token")
        request.state.user = user
        response = await call_next(request)
        return response