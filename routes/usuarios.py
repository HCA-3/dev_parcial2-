from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.UsuarioOut)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.crear_usuario(db, usuario)

@router.get("/tipo/{tipo}", response_model=list[schemas.UsuarioOut])
def listar_por_tipo(tipo: str, db: Session = Depends(get_db)):
    return crud.obtener_usuarios_por_tipo(db, tipo.capitalize())
