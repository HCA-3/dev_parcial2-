from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas

router = APIRouter(prefix="/tareas", tags=["tareas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{usuario_id}", response_model=schemas.Tarea)
def crear_tarea(usuario_id: int, tarea: schemas.TareaCreate, db: Session = Depends(get_db)):
    return crud.crear_tarea_para_usuario(db, tarea, usuario_id)

@router.get("/usuario/{usuario_id}", response_model=list[schemas.Tarea])
def listar_tareas(usuario_id: int, db: Session = Depends(get_db)):
    return crud.obtener_tareas_por_usuario(db, usuario_id)