from sqlalchemy.orm import Session
from . import models, schemas

# -------- Usuarios --------
def crear_usuario(db: Session, usuario: schemas.UsuarioCreate):
    nuevo = models.Usuario(**usuario.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_usuarios_por_tipo(db: Session, tipo: str):
    return db.query(models.Usuario).filter(models.Usuario.tipo == tipo).all()

def obtener_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

# -------- Tareas --------
def crear_tarea(db: Session, tarea: schemas.TareaCreate):
    nueva = models.Tarea(**tarea.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def obtener_tareas_por_usuario(db: Session, usuario_id: int):
    return db.query(models.Tarea).filter(models.Tarea.usuario_id == usuario_id).all()
