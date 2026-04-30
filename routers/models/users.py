from pydantic import BaseModel, Field


class Usuario(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=5, description="El nombre no puede estar vacío")
    edad: int = Field(..., gt=0, description="La edad debe ser un número positivo")