from sqlalchemy import select, func, distinct
from src.database import async_session
from src.models import Video, VideoSnapshot

# 1. Сколько всего видео
async def total_videos():
    async with async_session() as s:
        r = await s.execute(select(func.count(Video.id)))
        return r.scalar()

# 2. Видео креатора за период
async def videos_by_creator_period(creator_id, date_from, date_to):
    async with async_session() as s:
        r = await s.execute(
            select(func.count(Video.id))
            .where(
                Video.creator_id == creator_id,
                Video.video_created_at.between(date_from, date_to)
            )
        )
        return r.scalar()

# 3. Видео с просмотрами больше X
async def videos_with_views_gt(min_views):
    async with async_session() as s:
        r = await s.execute(
            select(func.count(Video.id))
            .where(Video.views_count > min_views)
        )
        return r.scalar()

# 4. Прирост просмотров за день
async def views_growth_on_date(date):
    async with async_session() as s:
        r = await s.execute(
            select(func.coalesce(func.sum(VideoSnapshot.delta_views_count), 0))
            .where(func.date(VideoSnapshot.created_at) == date)
        )
        return r.scalar()

# 5. Сколько видео имели новые просмотры в день
async def videos_with_new_views_on_date(date):
    async with async_session() as s:
        r = await s.execute(
            select(func.count(distinct(VideoSnapshot.video_id)))
            .where(
                func.date(VideoSnapshot.created_at) == date,
                VideoSnapshot.delta_views_count > 0
            )
        )
        return r.scalar()
