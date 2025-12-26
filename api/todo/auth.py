"""JWT authentication middleware and helpers.

This module provides:
- `verify_jwt(token)`: verifies JWT using configured keys/alg and returns payload.
- `AuthMiddleware`: FastAPI middleware that parses `Authorization` header,
  verifies token when present, and sets `request.state.current_user` to the
  token payload (dict). If a token is present but invalid, returns 401.
- `require_current_user(request)`: helper dependency that raises 401 when
  unauthenticated (for endpoints that must require auth).

Configuration (environment variables):
- `JWT_PUBLIC_KEY` : (optional) PEM public key string for RSA/EC verification.
- `JWT_SECRET` : (optional) HMAC secret (use if no public key provided).
- `JWT_ALGORITHM` : (optional) algorithm to expect, defaults to `RS256` if
  `JWT_PUBLIC_KEY` present, otherwise `HS256`.

This implements the verification strategy recommended by the BetterAuth spike
— backend‑issued JWTs are supported; the middleware does not issue tokens.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from jose import JWTError, jwt


JWT_PUBLIC_KEY = os.getenv("JWT_PUBLIC_KEY")
JWT_PRIVATE_KEY = os.getenv("JWT_PRIVATE_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def _get_algo() -> str:
    if JWT_ALGORITHM:
        return JWT_ALGORITHM
    return "RS256" if (JWT_PUBLIC_KEY or JWT_PRIVATE_KEY) else "HS256"


def _get_key(is_signing: bool = False) -> str | None:
    if is_signing:
        return JWT_PRIVATE_KEY if JWT_PRIVATE_KEY else (JWT_SECRET or BETTER_AUTH_SECRET)
    return JWT_PUBLIC_KEY if JWT_PUBLIC_KEY else (JWT_SECRET or BETTER_AUTH_SECRET)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a new JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    algo = _get_algo()
    key = _get_key(is_signing=True)
    if not key:
        raise HTTPException(
            status_code=500,
            detail="JWT signing not configured (missing JWT_PRIVATE_KEY, JWT_SECRET, or BETTER_AUTH_SECRET)",
        )
    
    encoded_jwt = jwt.encode(to_encode, key, algorithm=algo)
    return encoded_jwt


def verify_jwt(token: str) -> Dict[str, Any]:
    """Verify a JWT and return its payload.

    Raises `HTTPException(status_code=401)` on verification errors.
    """
    algo = _get_algo()
    key = _get_key(is_signing=False)
    if not key:
        raise HTTPException(
            status_code=500,
            detail="JWT verification not configured (missing JWT_PUBLIC_KEY, JWT_SECRET, or BETTER_AUTH_SECRET)",
        )
    try:
        payload = jwt.decode(token, key, algorithms=[algo])
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from exc
    return payload


class AuthMiddleware:
    """FastAPI HTTP middleware to parse and verify Bearer JWTs.

    Behavior:
    - If no Authorization header present: continue, `request.state.current_user` = None.
    - If Authorization: Bearer <token> present: verify token.
      - On success: set `request.state.current_user` to JWT payload (dict).
      - On failure: return 401 JSON response.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        auth: Optional[str] = request.headers.get("authorization")
        if auth and auth.lower().startswith("bearer "):
            token = auth.split(" ", 1)[1].strip()
            try:
                payload = verify_jwt(token)
            except HTTPException as exc:
                response = JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
                await response(scope, receive, send)
                return
            # Attach to scope state so endpoints/middlewares can access it
            scope.setdefault("state", {})
            scope["state"]["current_user"] = payload
        else:
            # No token present; ensure state exists
            scope.setdefault("state", {})
            scope["state"]["current_user"] = None

        await self.app(scope, receive, send)


def get_current_user_from_request(request: Request) -> Optional[Dict[str, Any]]:
    """Return `current_user` payload dict from request state, or None."""
    state = getattr(request, "state", None)
    if not state:
        return None
    return getattr(state, "current_user", None)


def require_current_user(request: Request) -> Dict[str, Any]:
    """Dependency: raise 401 if not authenticated, else return payload."""
    user = get_current_user_from_request(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user
