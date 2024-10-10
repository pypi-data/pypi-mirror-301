"""
任务调用api
"""

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, func, select

from mtmai.core.db import get_session
from mtmai.deps import CurrentUser
from mtmai.models.task import Task, TaskListResponse

router = APIRouter()


@router.get("/tasks", response_model=TaskListResponse)
async def task_list(
    *,
    session: Session = Depends(get_session),
    query: str = Query(default=""),
    skip: int = 0,
    user: CurrentUser,
    limit: int = Query(default=100, le=100),
):
    if user.is_superuser:
        count_statement = select(func.count()).select_from(Task)
        count = session.exec(count_statement).one()
        statement = select(Task).offset(skip).limit(limit)
        items = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count()).select_from(Task).where(Task.owner_id == user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Task).where(Task.owner_id == user.id).offset(skip).limit(limit)
        )
        items = session.exec(statement).all()

    return TaskListResponse(data=items, count=count)
