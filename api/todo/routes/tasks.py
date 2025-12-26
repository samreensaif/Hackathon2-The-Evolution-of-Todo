from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, SQLModel, select

from todo.auth import require_current_user
from todo.db import engine
from todo.models import Task

router = APIRouter()


class TaskCreateModel(Task):
    class Config:
        orm_mode = True


class TaskUpdateModel(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


def _user_id_from_payload(payload: dict) -> UUID:
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="Invalid token: missing sub claim")
    try:
        return UUID(sub)
    except Exception:
        # allow string user ids but ensure UUID required by DB
        raise HTTPException(status_code=401, detail="Invalid user id in token")


@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreateModel, current_user: dict = Depends(require_current_user)
):
    user_id = _user_id_from_payload(current_user)
    if not getattr(task_in, "title", None):
        raise HTTPException(status_code=400, detail="Title is required")

    task = Task(
        user_id=user_id,
        title=task_in.title,
        description=task_in.description,
        completed=task_in.completed or False,
    )
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
    return task


@router.get("/tasks")
def list_tasks(
    completed: Optional[bool] = Query(None),
    q: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    current_user: dict = Depends(require_current_user),
):
    user_id = _user_id_from_payload(current_user)
    with Session(engine) as session:
        stmt = select(Task).where(Task.user_id == user_id)
        if completed is not None:
            stmt = stmt.where(Task.completed == completed)
        if q:
            stmt = stmt.where(Task.title.ilike(f"%{q}%"))

        # Count total matches
        from sqlmodel import func

        count_stmt = select(func.count()).select_from(stmt.alias())
        total = session.exec(count_stmt).one()

        stmt = stmt.offset(offset).limit(limit)
        results = session.exec(stmt).all()
    return {"items": results, "total": total}


def _get_task_or_404(session: Session, task_id: UUID, user_id: UUID) -> Task:
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: UUID, current_user: dict = Depends(require_current_user)):
    user_id = _user_id_from_payload(current_user)
    with Session(engine) as session:
        task = _get_task_or_404(session, task_id, user_id)
    return task


@router.patch("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: UUID,
    task_in: TaskUpdateModel,
    current_user: dict = Depends(require_current_user),
):
    user_id = _user_id_from_payload(current_user)
    with Session(engine) as session:
        task = _get_task_or_404(session, task_id, user_id)
        updated = False
        if task_in.title is not None:
            if task_in.title == "":
                raise HTTPException(status_code=400, detail="Title cannot be empty")
            task.title = task_in.title
            updated = True
        if task_in.description is not None:
            task.description = task_in.description
            updated = True
        if task_in.completed is not None:
            task.completed = task_in.completed
            updated = True
        if updated:
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID, current_user: dict = Depends(require_current_user)):
    user_id = _user_id_from_payload(current_user)
    with Session(engine) as session:
        task = _get_task_or_404(session, task_id, user_id)
        session.delete(task)
        session.commit()
    return None
