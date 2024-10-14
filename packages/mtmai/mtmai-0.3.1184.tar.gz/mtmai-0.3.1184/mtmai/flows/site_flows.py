from typing import Any
import uuid

from fastapi import APIRouter, HTTPException, Query
from prefect import flow, task
from sqlmodel import func, select

from mtmai.deps import AsyncSessionDep, CurrentUser, OptionalUserDep
from mtmai.models.blog import BlogPostListResponse, Tag, TagListResponse
from mtmai.models.models import (
    Item,
)
from mtmai.models.site import (
    ListSiteHostRequest,
    ListSiteHostsResponse,
    ListSiteResponse,
    Site,
    SiteCreateRequest,
    SiteHost,
    SiteHostCreateRequest,
    SiteHostCreateResponse,
    SiteHostDeleteResponse,
    SiteHostUpdateRequest,
    SiteHostUpdateResponse,
    SiteItemPublic,
    SiteUpdateRequest,
)
@task
async def create_site_task(session: AsyncSessionDep, current_user: CurrentUser, item_in: SiteCreateRequest):
    item = Site.model_validate(item_in, update={"owner_id": current_user.id})
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


@flow
async def create_Site_flow(
    *, session: AsyncSessionDep, current_user: CurrentUser, item_in: SiteCreateRequest
) -> Any:
    """
    Create new site.
    """
    task1_result = await create_site_task(session, current_user, item_in)
    return task1_result