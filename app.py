from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Usuario, Tarea
from pydantic import BaseModel
from database import SessionLocal, engine
from typing import List

# Crear tablas en la base de datos
Usuario.metadata.create_all(bind=engine)
Tarea.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelos Pydantic
class UsuarioBase(BaseModel):
    nombre: str
    email: str

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioModel(UsuarioBase):
    id: int
    activo: bool
    premium: bool

    class Config:
        orm_mode = True

class TareaBase(BaseModel):
    titulo: str
    descripcion: str
    usuario_id: int

class TareaModel(TareaBase):
    id: int
    completada: bool

    class Config:
        orm_mode = True

# CRUD para Usuarios

@app.post("/usuarios/", response_model=UsuarioModel)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.get("/usuarios/", response_model=List[UsuarioModel])
def leer_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@app.get("/usuarios/{usuario_id}", response_model=UsuarioModel)
def leer_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.patch("/usuarios/{usuario_id}/estado", response_model=UsuarioModel)
def actualizar_estado(usuario_id: int, activo: bool, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_usuario.activo = activo
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.patch("/usuarios/{usuario_id}/premium", response_model=UsuarioModel)
def hacer_premium(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_usuario.premium = True
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.get("/usuarios/inactivos/", response_model=List[UsuarioModel])
def leer_usuarios_inactivos(db: Session = Depends(get_db)):
    return db.query(Usuario).filter(Usuario.activo == False).all()

@app.get("/usuarios/premium-inactivos/", response_model=List[UsuarioModel])
def leer_usuarios_premium_inactivos(db: Session = Depends(get_db)):
    return db.query(Usuario).filter(Usuario.premium == True, Usuario.activo == False).all()

# CRUD para Tareas

@app.post("/tareas/", response_model=TareaModel)
def crear_tarea(tarea: TareaBase, db: Session = Depends(get_db)):
    db_tarea = Tarea(**tarea.dict())
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea

@app.get("/tareas/", response_model=List[TareaModel])
def leer_tareas(db: Session = Depends(get_db)):
    return db.query(Tarea).all()

@app.get("/tareas/{tarea_id}", response_model=TareaModel)
def leer_tarea(tarea_id: int, db: Session = Depends(get_db)):
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

@app.patch("/tareas/{tarea_id}/completar", response_model=TareaModel)
def completar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    db_tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db_tarea.completada = True
    db.commit()
    db.refresh(db_tarea)
    return db_tarea