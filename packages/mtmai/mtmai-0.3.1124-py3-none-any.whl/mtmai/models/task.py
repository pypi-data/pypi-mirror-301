import uuid
from datetime import datetime

from sqlmodel import JSON, Column, Field, SQLModel

from mtmai.models.base_model import MtmBaseSqlModel


class TaskBase(SQLModel):
    name: str = Field(nullable=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    fulfilled_at: datetime | None = Field(default=None)
    site_id: str = Field(foreign_key="site.id", nullable=False, ondelete="CASCADE")
    status: str = Field(default="pending")
    priority: int = Field(default=0)
    # 任务参数
    payload: dict | None = Field(default={}, sa_column=Column(JSON))
    # 任务结果
    results: dict | None = Field(default={}, sa_column=Column(JSON))
    finished_at: datetime | None = Field(default=None)
    error: str | None = Field(default=None)


class Task(MtmBaseSqlModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    # owner_id: str = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    owner_id: uuid.UUID | None = Field( foreign_key="user.id",index=True,  nullable=False, ondelete="CASCADE")


class TaskItemPublic(TaskBase):
    pass


class TaskListResponse(SQLModel):
    data: list[TaskItemPublic]
    count: int


class TaskCreate(TaskBase):
    pass
