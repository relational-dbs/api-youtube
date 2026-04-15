from dataclasses import field

from fastapi import Depends, FastAPI, Query, Request
from fastapi import APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models.store import Articulo, Etiqueta
from models.users import Usuario
from persistence.db_connection import DBSessionManager, DBSessionMiddleware
from persistence.entities import Video

# 1. Creamos la instancia de la aplicación
app = FastAPI()
db_session_manager = DBSessionManager()
app.add_middleware(DBSessionMiddleware, db_session_manager=db_session_manager)


@app.get("/videos")
def get_videos(
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    db_session: Session = Depends(DBSessionMiddleware.get_db_session),
):
    videos = (
        db_session.query(Video)
        .order_by(Video.id.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    return videos
