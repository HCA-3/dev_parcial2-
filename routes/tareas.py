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

@router.post("/", response_model=schemas.TareaOut)
def crear_tarea(tarea: schemas.TareaCreate, db: Session = Depends(get_db)):
    usuario = crud.obtener_usuario(db, tarea.usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return crud.crear_tarea(db, tarea)

@router.get("/usuario/{usuario_id}", response_model=list[schemas.TareaOut])
def listar_tareas_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return crud.obtener_tareas_por_usuario(db, usuario_id)
