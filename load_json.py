import json
import asyncio
from datetime import datetime, timezone
import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database import async_session
from src.models import Video, VideoSnapshot


def parse_uuid(val):
    if isinstance(val, uuid.UUID):
        return val
    return uuid.UUID(val)


def parse_datetime(val):
    if not val:
        return None
    dt = datetime.fromisoformat(val)
    # Делаем все даты timezone-aware UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt


async def load_json():
    with open("data/videos.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    async with async_session() as session:
        for video in data.get("videos", []):
            # Проверяем, есть ли видео
            exists = await session.scalar(
                select(Video.id).where(Video.id == parse_uuid(video["id"]))
            )
            if exists:
                continue

            v = Video(
                id=parse_uuid(video["id"]),
                creator_id=parse_uuid(video["creator_id"]),
                video_created_at=parse_datetime(video["video_created_at"]),
                views_count=int(video.get("views_count") or 0),
                likes_count=int(video.get("likes_count") or 0),
                comments_count=int(video.get("comments_count") or 0),
                reports_count=int(video.get("reports_count") or 0),
                created_at=parse_datetime(video.get("created_at")),
                updated_at=parse_datetime(video.get("updated_at")),
            )

            session.add(v)

            snapshots = []
            for snap in video.get("snapshots", []):
                snapshots.append(
                    VideoSnapshot(
                        id=parse_uuid(snap["id"]),
                        video_id=parse_uuid(video["id"]),
                        views_count=int(snap.get("views_count") or 0),
                        likes_count=int(snap.get("likes_count") or 0),
                        comments_count=int(snap.get("comments_count") or 0),
                        reports_count=int(snap.get("reports_count") or 0),
                        delta_views_count=int(snap.get("delta_views_count") or 0),
                        delta_likes_count=int(snap.get("delta_likes_count") or 0),
                        delta_comments_count=int(snap.get("delta_comments_count") or 0),
                        delta_reports_count=int(snap.get("delta_reports_count") or 0),
                        created_at=parse_datetime(snap.get("created_at")),
                        updated_at=parse_datetime(snap.get("updated_at")),
                    )
                )

            session.add_all(snapshots)

        try:
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            print("Ошибка вставки:", e)
            raise


if __name__ == "__main__":
    asyncio.run(load_json())
