from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, crud, models
from .database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/usuarios", response_model=schemas.UsuarioOut)
def crear(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.crear_usuario(db, usuario)

@router.get("/usuarios", response_model=list[schemas.UsuarioOut])
def listar_todos(db: Session = Depends(get_db)):
    return crud.obtener_usuarios(db)

@router.get("/usuarios/inactivos", response_model=list[schemas.UsuarioOut])
def listar_inactivos(db: Session = Depends(get_db)):
    return crud.obtener_por_estado(db, estado="Inactivo")

@router.get("/usuarios/filtrados", response_model=list[schemas.UsuarioOut])
def listar_premium_inactivos(db: Session = Depends(get_db)):
    return crud.obtener_premium_inactivos(db)

@router.put("/usuarios/{usuario_id}", response_model=schemas.UsuarioOut)
def actualizar(usuario_id: int, datos: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = crud.actualizar_usuario(db, usuario_id, datos)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario
