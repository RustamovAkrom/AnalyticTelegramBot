from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
import uuid

class BaseModel(DeclarativeBase, AsyncAttrs):
    __abstract__ = True


class Video(BaseModel):
    __tablename__ = "videos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    creator_id = Column(UUID(as_uuid=True), nullable=False)

    # используем timezone=True, чтобы безопасно работать с UTC
    video_created_at = Column(DateTime(timezone=True), nullable=False)

    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    reports_count = Column(Integer, default=0)

    # автозаполняемые поля created_at / updated_at
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    snapshots = relationship(
        "VideoSnapshot",
        back_populates="video",
        cascade="all, delete-orphan"
    )


class VideoSnapshot(BaseModel):
    __tablename__ = "video_snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    video_id = Column(
        UUID(as_uuid=True),
        ForeignKey("videos.id", ondelete="CASCADE"),
        nullable=False
    )

    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    reports_count = Column(Integer, default=0)

    delta_views_count = Column(Integer, default=0)
    delta_likes_count = Column(Integer, default=0)
    delta_comments_count = Column(Integer, default=0)
    delta_reports_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    video = relationship("Video", back_populates="snapshots")
