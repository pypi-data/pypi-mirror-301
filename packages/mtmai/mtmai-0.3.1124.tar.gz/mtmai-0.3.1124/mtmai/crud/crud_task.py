from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.models.task import Task, TaskCreate


async def create_task(*, session: AsyncSession, task_create: TaskCreate, owner_id: str):
    db_item = Task.model_validate(task_create, update={"owner_id": owner_id})
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item
