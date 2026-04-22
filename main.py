from dataclasses import field
from typing import List
import uuid

from fastapi import Depends, FastAPI, Query, Request
from fastapi import APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models.store import Articulo, Etiqueta
from models.users import Usuario
from persistence.db_connection import DBSessionManager, DBSessionMiddleware
from persistence.entities import Video as EntityVideo
from models.videos import (
    VideoResponseModel as PydanticVideoResponseModel,
    VideoSimpleResponseModel as PydanticVideoSimpleResponseModel,
    VideoCreateModel as PydanticVideoCreateModel,
)
from routers import video
from util import logger

# 1. Creamos la instancia de la aplicación
app = FastAPI()

logger_session_manager = logger.LoggerSessionManager()

db_session_manager = DBSessionManager(
    logger_session_manager=logger_session_manager, echo=True
)
app.add_middleware(DBSessionMiddleware, db_session_manager=db_session_manager)

app.include_router(video.router)
