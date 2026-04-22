from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models.videos import (
    VideoResponseModel as PydanticVideoResponseModel,
    VideoSimpleResponseModel as PydanticVideoSimpleResponseModel,
    VideoCreateModel as PydanticVideoCreateModel,
)
from persistence.db_connection import DBSessionMiddleware
from persistence.entities import Video as EntityVideo
from persistence.db_connection import DBSessionMiddleware

router = APIRouter()


@router.get("/videos/{video_id}", response_model=PydanticVideoResponseModel)
def get_video(
    video_id: int,
    db_session: Session = Depends(DBSessionMiddleware.get_db_session),
):
    entityVideo = (
        db_session.query(EntityVideo).filter(EntityVideo.id == video_id).first()
    )
    if not entityVideo:
        raise HTTPException(status_code=404, detail="Video not found")
    return entityVideo


@router.get("/videos", response_model=List[PydanticVideoSimpleResponseModel])
def get_videos(
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    db_session: Session = Depends(DBSessionMiddleware.get_db_session),
):
    entityVideos = (
        db_session.query(EntityVideo)
        .order_by(EntityVideo.id.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    return entityVideos


@router.post("/videos", response_model=PydanticVideoResponseModel)
def create_video(
    video: PydanticVideoCreateModel,
    db_session: Session = Depends(DBSessionMiddleware.get_db_session),
):
    entityVideo = EntityVideo(**{**video.dict(), "uuid": uuid.uuid4(), "creador_id": 1})
    db_session.add(entityVideo)
    db_session.commit()
    db_session.refresh(entityVideo)
    return entityVideo


@router.put("/videos/{video_id}", response_model=PydanticVideoResponseModel)
def update_video(
    video_id: int,
    video: PydanticVideoCreateModel,
    db_session: Session = Depends(DBSessionMiddleware.get_db_session),
):
    entityVideo = (
        db_session.query(EntityVideo).filter(EntityVideo.id == video_id).first()
    )
    if not entityVideo:
        raise HTTPException(status_code=404, detail="Video not found")
    for key, value in video.dict().items():
        setattr(entityVideo, key, value)
    db_session.commit()
    db_session.refresh(entityVideo)

    return entityVideo
