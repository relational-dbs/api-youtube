from pydantic import BaseModel

class Etiqueta(BaseModel):
    nombre: str
    color: str
    
class Articulo(BaseModel):
    titulo: str
    contenido: str
    etiquetas: list[Etiqueta] = []