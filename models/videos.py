
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class VideoCreateModel(BaseModel):
    titulo: str
    descripcion: str
    fecha_creacion: datetime
    duracion: int
    
    model_config = ConfigDict(from_attributes=True)
    
class VideoResponseModel(BaseModel):
    id: int
    uuid: UUID
    titulo: str
    descripcion: str
    fecha_creacion: datetime
    duracion: int
    creador_id: int
    
    model_config = ConfigDict(from_attributes=True)

class VideoSimpleResponseModel(BaseModel):
    
    titulo: str
    descripcion: str

    model_config = ConfigDict(from_attributes=True)