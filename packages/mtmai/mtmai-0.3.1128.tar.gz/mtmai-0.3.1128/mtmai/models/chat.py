import uuid
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel
from sqlmodel import JSON, Column, Field

from mtmai.models.agent import CopilotScreen
from mtmai.models.base_model import MtmBaseSqlModel


class ChatThread(MtmBaseSqlModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(nullable=True)
    user_id: uuid.UUID | None = Field(
        foreign_key="user.id", index=True, nullable=False, ondelete="CASCADE"
    )
    user_identifier: str = Field(nullable=True)
    tags: list[str] = Field(default=[], sa_column=Column(JSON))
    meta: dict | None = Field(default={}, sa_column=Column(JSON))

    # _upsert_index_elements = {"id"}


class ChatStep(MtmBaseSqlModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    type: str = Field(max_length=255)
    thread_id: uuid.UUID = Field(...)
    parent_id: uuid.UUID | None = Field(default=None)
    disable_feedback: bool = Field(...)
    streaming: bool = Field(...)
    wait_for_answer: bool | None = Field(default=None)
    is_error: bool | None = Field(default=None)
    meta: dict | None = Field(default=None, sa_column=Column(JSON))
    tags: list[str] | None = Field(default=[], sa_column=Column(JSON))
    input: str | None = Field(default=None)
    output: str | None = Field(default=None)
    start: datetime | None = Field(default=None)
    end: datetime | None = Field(default=None)
    generation: dict | None = Field(default=None, sa_column=Column(JSON))
    show_input: str | None = Field(default=None)
    language: str | None = Field(default=None)
    indent: int | None = Field(default=None)

    _upsert_index_elements = {"id"}



class ChatElement(MtmBaseSqlModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    thread_id: uuid.UUID | None = Field(default=None)
    type: str | None = Field(default=None)
    url: str | None = Field(default=None)
    chainlit_key: str | None = Field(default=None)
    name: str = Field(...)
    display: str | None = Field(default=None)
    object_key: str | None = Field(default=None)
    size: str | None = Field(default=None)
    page: int | None = Field(default=None)
    language: str | None = Field(default=None)
    for_id: uuid.UUID | None = Field(default=None)
    mime: str | None = Field(default=None)

    _upsert_index_elements = {"id"}


class ChatFeedback(MtmBaseSqlModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    for_id: uuid.UUID = Field(...)
    thread_id: uuid.UUID = Field(...)
    value: int = Field(...)
    comment: str | None = Field(default=None)

    _upsert_index_elements = {"id"}


class Starter(BaseModel):
    """Specification for a starter that can be chosen by the user at the thread start."""

    label: str
    message: str
    icon: Optional[str] = None


class ChatProfile(MtmBaseSqlModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(...)
    description: str = Field(...)
    icon: str | None = Field(default=None)
    default: bool | None = Field(default=False)
    # starters: list[dict] = Field(default=[])
    starters: list[dict] | None = Field(default=None, sa_column=Column(JSON))


class ChatProfilesResponse(BaseModel):
    count: int
    data: list[ChatProfile]


class ThreadUIState(BaseModel):
    """ThreadView 的UI 状态"""

    enableChat: bool | None = False
    enableScrollToBottom: bool = True
    title: str | None = None
    description: str | None = None
    icons: str | None = None
    layout: str | None = None
    theme: str | None = None
    isOpen: bool | None = None
    screens: list[CopilotScreen] = Field(default_factory=list)
    activateViewName: str | None = "/"

    # 对话输入框的位置
    inputPosition: Literal["inline", "bottom"] | None = "bottom"
    fabEnabled: bool = True
    fabIcon: str | None = None
    fabAction: str | None = None
    fabDisplayText: str | None = None
    fabDisplayIcon: str | None = None
    fabDisplayColor: str | None = None
    fabDisplayAction: str | None = None
    fabDisplayPosition: Literal["top", "bottom"] | None = "bottom"

    # play data

    playDataType: Literal["post", "demoArticle"] | None = None
    playData: dict | None = Field(default=None, sa_column=Column(JSON))
