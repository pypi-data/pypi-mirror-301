from mimetypes import add_type
from typing import Any, Literal

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlmodel import func, select

from mtmai.core.logging import get_logger
from mtmai.deps import AsyncSessionDep, CurrentUser
from mtmai.models.search_index import SearchIndex, SearchIndexResponse, SearchRequest

router = APIRouter()
logger = get_logger()
sql_schema = """
CREATE TABLE search_index (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,  -- 'site', 'thread', 'task' 等
    title TEXT NOT NULL,
    content TEXT,
    url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    search_vector tsvector
);

CREATE INDEX search_vector_idx ON search_index USING GIN (search_vector);
"""
# 创建一个触发器函数来自动更新 search_vector：
sql_trigger = """
CREATE FUNCTION search_vector_update() RETURNS trigger AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.content, '')), 'B');
    RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER search_vector_update
BEFORE INSERT OR UPDATE ON search_index
FOR EACH ROW EXECUTE FUNCTION search_vector_update();
"""


@router.post("/", response_model=SearchIndexResponse)
async def search(
    session: AsyncSessionDep, current_user: CurrentUser, req: SearchRequest
) -> Any:
    """
    综合搜索, 支持搜索站点, 文档, 知识库。返回搜索结果的摘要条目。
    前端，通常点击条目后，打开详细操作页
    参考： https://www.w3cschool.cn/article/34124192.html

    TODO: 可以考虑添加高亮显示的功能。
    """
    search_query = req.q
    data_type = req.dataType
    offset = req.skip
    limit = req.limit
    app = req.app or "mtmai_copilot"

    query = select(SearchIndex)

    if data_type:
        query = query.where(SearchIndex.content_type == data_type)

    if search_query:
        query = query.where(
            func.to_tsvector("english", SearchIndex.content_summary).op(
                "@@"
            )(func.plainto_tsquery("english", search_query))
        )
    query = query.where(SearchIndex.is_deleted == False)
    query = query.where(SearchIndex.owner_id == current_user.id)


    # 添加排序逻辑
    if search_query:
        query = query.order_by(
            func.ts_rank(
                func.to_tsvector("english", SearchIndex.content_summary),
                func.plainto_tsquery("english", search_query)
            ).desc()
        )
    else:
        # 无搜索词，按创建时间排序
        query = query.order_by(SearchIndex.created_at.desc())


    # 获取总数
    total_count = await session.scalar(select(func.count()).select_from(query.subquery()))

    query = query.offset(offset).limit(limit)

    # 获取总数


    result = await session.exec(query)
    items = result.all()

    # 查询搜索索引
    # index_sql = text("""
    # SELECT id, type, title,
    #        ts_headline('english', content, plainto_tsquery(:query)) as snippet,
    #        url,
    #        ts_rank(search_vector, plainto_tsquery(:query)) as rank
    # FROM search_index
    # WHERE search_vector @@ plainto_tsquery(:query)
    # """)

    # # 查询原始表（这里以 sites 表为例）
    # sites_sql = text("""
    # SELECT id, 'site' as type, title,
    #        left(description, 200) as snippet,
    #        url,
    #        0 as rank
    # FROM sites
    # WHERE to_tsvector('english', title || ' ' || description) @@ plainto_tsquery(:query)
    # AND id NOT IN (SELECT id FROM search_index WHERE type = 'site')
    # """)

    # # 执行查询
    # index_result = await session.exec(index_sql, {"query": query})
    # sites_result = await session.exec(sites_sql, {"query": query})

    # # 合并结果
    # all_items = [dict(row) for row in index_result.mappings()] + [dict(row) for row in sites_result.mappings()]

    # # 排序和分页
    # sorted_items = sorted(all_items, key=lambda x: x['rank'], reverse=True)
    # paginated_items = sorted_items[offset:offset+limit]

    # items = [SearchResultItem(**item) for item in paginated_items]

    # # 计算总数
    # total = len(all_items)
    # total_pages = (total + request.per_page - 1) // request.per_page

    # 使用 jsonable_encoder 确保正确序列化
    serialized_items = jsonable_encoder(items)
    return SearchIndexResponse(
        data=serialized_items,
        count=total_count,
    )


class RetrieveRequest(BaseModel):
    format: Literal["markdown", "html", "raw", "json"] = "markdown"
    query: str
    tags: str


class RetrieveResponse(BaseModel):
    content: str


# @router.post("/retrieve", response_model=SearchIndexResponse)
# async def retrieve(
#     session: AsyncSessionDep, current_user: CurrentUser, req: SearchRequest
# ) -> Any:
#     """ "
#     大语言 embedding 召回内容
#     """
#     # pass
