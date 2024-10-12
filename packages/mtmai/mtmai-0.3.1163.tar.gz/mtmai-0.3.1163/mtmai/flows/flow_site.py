"""
工作流： 站点管理
"""
import asyncio
from datetime import timedelta
from numpy import rec
from prefect import flow, task, get_run_logger,serve
from prefect.tasks import task_input_hash
import asyncio
from textwrap import dedent

from pydantic import BaseModel

from mtmai.agents.ctx import mtmai_context
from mtmai.agents.tools.tools import get_tools
from mtmai.core.logging import get_logger
from mtmai.crewai import Agent, Crew, Process, Task
from mtmai.flows.article_gen import article_gen_outline
from mtmai.models.book_gen import BookOutline, Chapter, ChapterOutline, GenBookState, WriteOutlineRequest
from mtmai.models.graph_config import Section

@flow
async def flow_cms_site():
    """
    给定站点，自动操作
    包括： 1:自动发布文章
            2 自动更新文章
            3 自动删除文章
    """

    logger = get_run_logger()
    logger.info("flow_article_gen start ...")

    site_id = "123"
    site_type = "wordpress"

