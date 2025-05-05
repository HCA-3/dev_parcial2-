from sqlalchemy.orm import Session
from . import models, schemas

def crear_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def obtener_usuarios(db: Session):
    return db.query(models.Usuario).all()

def obtener_por_estado(db: Session, estado: str):
    return db.query(models.Usuario).filter(models.Usuario.estado == estado).all()

def obtener_premium_inactivos(db: Session):
    return db.query(models.Usuario).filter(models.Usuario.tipo == "Premium", models.Usuario.estado == "Inactivo").all()

def actualizar_usuario(db: Session, usuario_id: int, datos: schemas.UsuarioUpdate):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if usuario:
        usuario.estado = datos.estado
        usuario.tipo = datos.tipo
        db.commit()
        db.refresh(usuario)
    return usuario
