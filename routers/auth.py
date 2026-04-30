from datetime import datetime, timedelta
import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from sqlalchemy.orm import Session
from persistence.db_connection import DBSessionMiddleware
from persistence.entities import Usuario

JWT_SECRET_KEY = "clave_super_secreta_para_firmar_el_jwt"  # Cambia esto por una clave segura en producción
JWT_ALGORITHM = "HS256"

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(DBSessionMiddleware.get_db_session),
):
    # 1. Buscamos al usuario en la Base de Datos
    user = db.query(Usuario).filter(Usuario.correo == form_data.username).first()

    # 2. Verificamos que exista y que la contraseña sea correcta
    if not user or not bcrypt.checkpw(
        form_data.password.encode("utf-8"), user.contrasena.encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    # 3. Preparamos el Payload con fecha de caducidad (ej. 30 min)
    issued_timestamp = datetime.utcnow() + timedelta(minutes=30)
    payload = {
        "sub": user.correo,
        "issued": issued_timestamp.timestamp(),
    }  # 'sub' es el sujeto del token, comúnmente el username o user_id

    # 4. Firmamos el JWT y lo entregamos en el formato oficial
    token_firmado = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return {"access_token": token_firmado, "token_type": "bearer"}


def validate_token(token: str = Depends(oauth2_scheme), db: Session = Depends(DBSessionMiddleware.get_db_session)):
    try:
        # 1. Intentamos desempaquetar el JWT
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
    # 2. Buscamos en BD con SQLAlchemy y retornamos
    user = db.query(Usuario).filter(Usuario.correo == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    return user