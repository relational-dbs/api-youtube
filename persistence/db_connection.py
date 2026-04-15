from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from entities import Video

DATABASE_URL = "postgresql+psycopg://postgres:password@localhost:5423/youtube"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionLocal()

for video in session.query(Video).limit(2).all():
    print(video.titulo)

# query = text("SELECT titulo FROM video LIMIT 2")
# with engine.connect() as connection:
#     result = connection.execute(query)
#     for row in result:
#         print(row)