from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.llm.embedding import embedding_hf
from mtmai.models.blog import Post
from mtmai.models.models import Document, DocumentIndex
from mtmai.models.search_index import SearchIndex


async def create_post_search_index(db: AsyncSession, post: Post, post_content: str):
    search_index = SearchIndex(
        content_type="post",
        content_id=post.id,
        title=post.title,
        content=post_content,
    )
    db.add(search_index)
    await db.commit()
    await db.refresh(search_index)
    return search_index


async def embeding_post(*, session: AsyncSession, doc_id, content: str):
    """创建文档索引 基于大语言 embedding 的 索引（可能过时，改用 SearchIndex）"""

    # Create Document
    doc = Document(content=content)
    session.add(doc)
    await session.flush()  # Flush to get the id without committing

    embedding_model = "mixedbread-ai/mxbai-embed-large-v1"
    embedding_result = await embedding_hf(inputs=[content], model_name=embedding_model)
    doc_index = DocumentIndex(
        document_id=doc_id, embedding=embedding_result[0], emb_model=embedding_model
    )
    session.add(doc_index)
