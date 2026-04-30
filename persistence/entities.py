import datetime
import uuid as uuid_

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKeyConstraint,
    Index,
    PrimaryKeyConstraint,
    SmallInteger,
    String,
    Text,
    Uuid,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = "usuario"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="usuario_pkey"),
        Index("usuario_correo_key", "correo", unique=True),
        Index("usuario_correo_like", "correo"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    correo: Mapped[str] = mapped_column(String(254), nullable=False)
    contrasena: Mapped[str] = mapped_column(String(100), nullable=False)

    suscripcion_creador: Mapped[list["Suscripcion"]] = relationship(
        "Suscripcion", foreign_keys="[Suscripcion.creador_id]", back_populates="creador"
    )
    suscripcion_suscriptor: Mapped[list["Suscripcion"]] = relationship(
        "Suscripcion",
        foreign_keys="[Suscripcion.suscriptor_id]",
        back_populates="suscriptor",
    )
    video: Mapped[list["Video"]] = relationship("Video", back_populates="creador")
    comentario: Mapped[list["Comentario"]] = relationship(
        "Comentario", back_populates="usuario"
    )
    reproduccion: Mapped[list["Reproduccion"]] = relationship(
        "Reproduccion", back_populates="usuario"
    )


class Suscripcion(Base):
    __tablename__ = "suscripcion"
    __table_args__ = (
        ForeignKeyConstraint(
            ["creador_id"],
            ["usuario.id"],
            ondelete="CASCADE",
            onupdate="RESTRICT",
            name="suscripcion_creador_id_fkey",
        ),
        ForeignKeyConstraint(
            ["suscriptor_id"],
            ["usuario.id"],
            ondelete="CASCADE",
            onupdate="RESTRICT",
            name="suscripcion_suscriptor_id_fkey",
        ),
        PrimaryKeyConstraint("id", name="suscripcion_pkey"),
        Index("suscripcion_creador_id", "creador_id"),
        Index("suscripcion_suscriptor_id", "suscriptor_id"),
        Index(
            "suscripcion_suscriptor_id_creador_id_uniq",
            "suscriptor_id",
            "creador_id",
            unique=True,
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    creador_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    suscriptor_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    creador: Mapped["Usuario"] = relationship(
        "Usuario", foreign_keys=[creador_id], back_populates="suscripcion_creador"
    )
    suscriptor: Mapped["Usuario"] = relationship(
        "Usuario", foreign_keys=[suscriptor_id], back_populates="suscripcion_suscriptor"
    )

class Pais(Base):
    __tablename__ = "pais"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pais_pkey"),
        Index("pais_nombre_key", "nombre", unique=True),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)

class Video(Base):
    __tablename__ = "video"
    __table_args__ = (
        ForeignKeyConstraint(
            ["creador_id"],
            ["usuario.id"],
            ondelete="CASCADE",
            onupdate="RESTRICT",
            name="video_creador_id_fkey",
        ),
        PrimaryKeyConstraint("id", name="video_pkey"),
        Index("video_creador_id", "creador_id"),
        Index("video_uuid_key", "uuid", unique=True),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    uuid: Mapped[uuid_.UUID] = mapped_column(Uuid, nullable=False)
    titulo: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(
        DateTime(True), nullable=False
    )
    duracion: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    creador_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    creador: Mapped["Usuario"] = relationship("Usuario", back_populates="video")
    comentario: Mapped[list["Comentario"]] = relationship(
        "Comentario", back_populates="video"
    )
    reproduccion: Mapped[list["Reproduccion"]] = relationship(
        "Reproduccion", back_populates="video"
    )


class Comentario(Base):
    __tablename__ = "comentario"
    __table_args__ = (
        ForeignKeyConstraint(
            ["usuario_id"],
            ["usuario.id"],
            ondelete="CASCADE",
            onupdate="RESTRICT",
            name="comentario_usuario_id_fkey",
        ),
        ForeignKeyConstraint(
            ["video_id"],
            ["video.id"],
            ondelete="CASCADE",
            onupdate="RESTRICT",
            name="comentario_video_id_fkey",
        ),
        PrimaryKeyConstraint("id", name="comentario_pkey"),
        Index("comentario_usuario_id", "usuario_id"),
        Index("comentario_video_id", "video_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(
        DateTime(True), nullable=False
    )
    usuario_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    video_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    
    idioma: Mapped[str] = mapped_column(String(10), nullable=True)

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="comentario")
    video: Mapped["Video"] = relationship("Video", back_populates="comentario")


class Reproduccion(Base):
    __tablename__ = "reproduccion"
    __table_args__ = (
        ForeignKeyConstraint(
            ["usuario_id"],
            ["usuario.id"],
            ondelete="CASCADE",
            onupdate="RESTRICT",
            name="reproduccion_usuario_id_fkey",
        ),
        ForeignKeyConstraint(
            ["video_id"],
            ["video.id"],
            ondelete="CASCADE",
            onupdate="RESTRICT",
            name="reproduccion_video_id_fkey",
        ),
        PrimaryKeyConstraint("id", name="reproduccion_pkey"),
        Index("reproduccion_usuario_id", "usuario_id"),
        Index("reproduccion_video_id", "video_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fecha_reproduccion: Mapped[datetime.datetime] = mapped_column(
        DateTime(True), nullable=False
    )
    dispositivo_reproduccion: Mapped[str] = mapped_column(String(100), nullable=False)
    usuario_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    video_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="reproduccion")
    video: Mapped["Video"] = relationship("Video", back_populates="reproduccion")
