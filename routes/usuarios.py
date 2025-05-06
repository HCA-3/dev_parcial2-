from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Usuario)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.crear_usuario(db, usuario)

@router.get("/", response_model=list[schemas.Usuario])
def listar_usuarios(db: Session = Depends(get_db)):
    return crud.obtener_usuarios(db)

@router.get("/{usuario_id}", response_model=schemas.Usuario)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.obtener_usuario_por_id(db, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@router.put("/{usuario_id}", response_model=schemas.Usuario)
def actualizar_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud.actualizar_usuario(db, usuario_id, usuario)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    eliminado = crud.eliminar_usuario(db, usuario_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado"}

@router.patch("/{usuario_id}/estado", response_model=schemas.Usuario)
def actualizar_estado_usuario(usuario_id: int, estado: str, db: Session = Depends(get_db)):
    db_usuario = crud.obtener_usuario_por_id(db, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_usuario.estado = estado
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.patch("/{usuario_id}/premium", response_model=schemas.Usuario)
def hacer_premium(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.obtener_usuario_por_id(db, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_usuario.tipo = "Premium"
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.get("/inactivos/", response_model=list[schemas.Usuario])
def listar_usuarios_inactivos(db: Session = Depends(get_db)):
    return crud.obtener_usuarios_por_estado(db, "Inactive")

@router.get("/premium-inactivos/", response_model=list[schemas.Usuario])
def listar_premium_inactivos(db: Session = Depends(get_db)):
    return crud.obtener_usuarios_premium_inactivos(db)