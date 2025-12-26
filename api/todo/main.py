"""FastAPI app for Todo API (Phase II)."""

from dotenv import load_dotenv

load_dotenv()


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from todo.auth import AuthMiddleware, get_current_user_from_request
from todo.routes.auth import router as auth_router
from todo.routes.tasks import router as tasks_router

# Create FastAPI app
app = FastAPI(title="Todo API (Phase II)")

# --------------------------------------------------
# CORS Middleware (MUST be first)
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Authentication Middleware
# --------------------------------------------------
app.add_middleware(AuthMiddleware)


# --------------------------------------------------
# Health Check
# --------------------------------------------------
@app.get("/health")
def health(request: Request):
    user = get_current_user_from_request(request)
    return {
        "status": "ok",
        "authenticated": bool(user),
    }


# --------------------------------------------------
# API Routers
# --------------------------------------------------
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(tasks_router, prefix="/api/v1", tags=["tasks"])
