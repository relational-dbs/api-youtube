from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, UUID
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import MappedColumn, relationship

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    correo = Column(String, nullable=False, index=True)
    contrasena = Column(String, nullable=False)

    videos = relationship("Video", back_populates="usuario")

class Video(Base):
    __tablename__ = "video"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID, index=True)
    titulo = Column(String, index=True)
    descripcion = Column(String)
    fecha_creacion = Column(TIMESTAMP(timezone=True))
    duracion = Column(Integer)
    creador_id = Column(Integer, ForeignKey("usuario.id"))

    usuario = relationship("Usuario", back_populates="videos", foreign_keys=[creador_id])
