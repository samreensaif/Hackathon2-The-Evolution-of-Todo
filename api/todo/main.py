"""Placeholder FastAPI app for Todo API (scaffolded by T001)."""

from fastapi import FastAPI

app = FastAPI(title="Todo API (Phase II)")


@app.get("/health")
def health():
    return {"status": "ok"}
