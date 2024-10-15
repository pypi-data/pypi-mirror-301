from datetime import datetime

from sqlmodel import Field, SQLModel


class ListviewItem(SQLModel):
    title: str
    sub_title: str | None = None
    description: str | None = None
    updated_at: datetime = Field(default=datetime.now())


class ListItemResponse(SQLModel):
    count: int
    items: list[ListviewItem]
