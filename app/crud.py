from sqlalchemy.orm import Session
from app import models, schemas

# Operaciones para Usuarios
def crear_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def obtener_usuarios(db: Session):
    return db.query(models.Usuario).all()

def obtener_usuario_por_id(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def actualizar_usuario(db: Session, usuario_id: int, usuario: schemas.UsuarioCreate):
    db_usuario = obtener_usuario_por_id(db, usuario_id)
    if db_usuario:
        for key, value in usuario.dict().items():
            setattr(db_usuario, key, value)
        db.commit()
        db.refresh(db_usuario)
    return db_usuario

def eliminar_usuario(db: Session, usuario_id: int):
    db_usuario = obtener_usuario_por_id(db, usuario_id)
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
        return True
    return False

def obtener_usuarios_por_estado(db: Session, estado: str):
    return db.query(models.Usuario).filter(models.Usuario.estado == estado).all()

def obtener_usuarios_premium_inactivos(db: Session):
    return db.query(models.Usuario).filter(
        models.Usuario.tipo == "Premium",
        models.Usuario.estado == "Inactive"
    ).all()

# Operaciones para Tareas
def crear_tarea_para_usuario(db: Session, tarea: schemas.TareaCreate, usuario_id: int):
    db_tarea = models.Tarea(**tarea.dict(), usuario_id=usuario_id)
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea

def obtener_tareas_por_usuario(db: Session, usuario_id: int):
    return db.query(models.Tarea).filter(models.Tarea.usuario_id == usuario_id).all()