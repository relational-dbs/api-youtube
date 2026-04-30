from fastapi import FastAPI
from persistence.db_connection import DBSessionManager, DBSessionMiddleware
from routers import auth, videos
from util import logger

logger_session_manager = logger.LoggerSessionManager()
db_session_manager = DBSessionManager(
    logger_session_manager=logger_session_manager, echo=False
)

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_session_manager=db_session_manager)
app.include_router(videos.router)
app.include_router(auth.router)
