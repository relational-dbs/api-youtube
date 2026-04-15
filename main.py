from fastapi import FastAPI
from fastapi import APIRouter
from pydantic import BaseModel, Field
from models.store import Articulo, Etiqueta
from models.users import Usuario

# 1. Creamos la instancia de la aplicación
app = FastAPI()

router = APIRouter(prefix="/datos", tags=["Usuarios"])


@app.get("/articulos")
def get_articulos() -> list[Articulo]:
    articulo = Articulo(
        titulo="Mi primer artículo",
        contenido="Este es el contenido del artículo",
        etiquetas=[
            Etiqueta(nombre="Python", color="azul"),
            Etiqueta(nombre="FastAPI", color="rojo"),
        ],
    )
    return [articulo]


@app.post("/usuarios")
def crear_usuario(usuario: Usuario):
    return usuario


# 2. Definimos la ruta (Endpoint) y el verbo HTTP (GET)
@app.post("/testpath")
def leer_raiz():
    # 3. Retornamos un diccionario (Se convierte a JSON)
    return {"mensaje": "¡Hola, Clase!"}


# Ejemplo: GET /usuarios/12
@app.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int):
    return {"id": usuario_id, "nombre": "Juan"}


# Ejemplo: PUT /usuarios/12
@app.put("/usuarios/{usuario_id}")
def actualizar_usuario(usuario_id: int):
    return "Usuario actualizado"


# Ejemplo: GET /items?limit=10&skip=5
@app.get("/items")
def listar_items(limit: int = 10, skip=12):
    return {"limit": limit, "skip": skip}


@router.get("/lista", status_code=418)
def listar_usuarios():
    return [{"nombre": "Ana"}, {"nombre": "Juan"}]


app.include_router(router=router)
