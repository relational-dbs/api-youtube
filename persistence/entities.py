from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String  
from sqlalchemy import TIMESTAMP

Base = declarative_base()

class Video(Base):
    __tablename__ = "video"
    id = Column(Integer, primary_key=True, auto_increment=True)
    uuid = Column(String, index=True)
    titulo = Column(String, index=True)
    descripcion = Column(String)
    fecha_creacion = Column(TIMESTAMP(timezone=True))
    duracion = Column(Integer)
    creador_id = Column(Integer, index=True)
