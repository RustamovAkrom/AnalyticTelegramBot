# src/metrics.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from .models import Video, VideoSnapshot
from datetime import datetime
# src/metrics.py
from typing import Optional

# Общее количество видео
async def total_videos(session: AsyncSession) -> int:
    result = await session.execute(select(func.count()).select_from(Video))
    return result.scalar_one()

# Количество видео у конкретного креатора за период
async def videos_by_creator(session: AsyncSession, creator_id: str, start: datetime, end: datetime) -> int:
    result = await session.execute(
        select(func.count())
        .select_from(Video)
        .where(
            and_(
                Video.creator_id == creator_id,
                Video.video_created_at >= start,
                Video.video_created_at <= end
            )
        )
    )
    return result.scalar_one()

# Количество видео с просмотрами больше N
async def videos_over_views(session: AsyncSession, min_views: int) -> int:
    result = await session.execute(
        select(func.count()).select_from(Video).where(Video.views_count > min_views)
    )
    return result.scalar_one()

# Суммарный прирост просмотров за период
async def total_views_growth(session: AsyncSession, start: datetime, end: datetime) -> int:
    result = await session.execute(
        select(func.sum(VideoSnapshot.delta_views_count))
        .where(and_(VideoSnapshot.created_at >= start, VideoSnapshot.created_at <= end))
    )
    return result.scalar_one() or 0

# Количество видео с приростом просмотров за период
async def videos_with_growth(session: AsyncSession, start: datetime, end: datetime) -> int:
    result = await session.execute(
        select(func.count(func.distinct(VideoSnapshot.video_id)))
        .where(and_(VideoSnapshot.created_at >= start,
                    VideoSnapshot.created_at <= end,
                    VideoSnapshot.delta_views_count > 0))
    )
    return result.scalar_one() or 0

# Количество видео у креатора с просмотрами больше N
async def videos_by_creator_over_views(
    session: AsyncSession,
    creator_id: str,
    min_views: int,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None
) -> int:
    query = select(func.count()).select_from(Video).where(
        Video.creator_id == creator_id,
        Video.views_count > min_views
    )

    if start:
        query = query.where(Video.video_created_at >= start)
    if end:
        query = query.where(Video.video_created_at <= end)

    result = await session.execute(query)
    return result.scalar_one()

async def generate_context(session: AsyncSession) -> str:
    total = await total_videos(session)
    top_videos_100k = await videos_over_views(session, 100_000)

    context = f"""
Текущая статистика по видео-креаторам:
- Всего видео: {total}
- Видео с более чем 100_000 просмотров: {top_videos_100k}
"""
    return context.strip()
