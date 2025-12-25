"""Placeholder FastAPI app for Todo API (scaffolded by T001)."""

from fastapi import FastAPI, Request

from todo.auth import AuthMiddleware, get_current_user_from_request

app = FastAPI(title="Todo API (Phase II)")


@app.middleware("http")
async def attach_auth(request: Request, call_next):
    # Lightweight wrapper to make AuthMiddleware behavior available via FastAPI
    # request state. We use AuthMiddleware logic via the class callable for
    # consistency with ASGI usage.
    # If JWT is present and valid, `request.state.current_user` will be set.
    # If JWT is present and invalid, the AuthMiddleware would return 401.
    # Here we'll manually parse header and set request.state.current_user to
    # preserve behavior without changing other ASGI wiring.
    from todo.auth import verify_jwt

    auth = request.headers.get("authorization")
    if auth and auth.lower().startswith("bearer "):
        token = auth.split(" ", 1)[1].strip()
        try:
            payload = verify_jwt(token)
            request.state.current_user = payload
        except Exception:
            from fastapi.responses import JSONResponse

            return JSONResponse({"detail": "Invalid or expired token"}, status_code=401)
    else:
        request.state.current_user = None

    response = await call_next(request)
    return response


@app.get("/health")
def health(request: Request):
    user = get_current_user_from_request(request)
    return {"status": "ok", "user": bool(user)}
