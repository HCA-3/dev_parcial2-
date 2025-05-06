from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
import models
from database import SessionLocal, engine
import logging
import os

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Usuarios y Tareas",
    description="API para gestión de usuarios y sus tareas",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class UsuarioBase(BaseModel):
    nombre: str
    email: str

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id: int
    activo: bool
    premium: bool

    class Config:
        orm_mode = True

class TareaBase(BaseModel):
    titulo: str
    descripcion: str
    usuario_id: int

class Tarea(TareaBase):
    id: int
    completada: bool

    class Config:
        orm_mode = True

# Dependencia DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints básicos
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Usuarios y Tareas"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Endpoints de Usuarios (CRUD completo)
@app.post("/usuarios/", response_model=Usuario)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        db_usuario = models.Usuario(**usuario.dict())
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear usuario: {str(e)}")
        raise HTTPException(status_code=400, detail="Error al crear usuario")

@app.get("/usuarios/", response_model=List[Usuario])
def leer_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()

@app.get("/usuarios/{usuario_id}", response_model=Usuario)
def leer_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.patch("/usuarios/{usuario_id}/estado", response_model=Usuario)
def actualizar_estado(usuario_id: int, activo: bool, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.activo = activo
    db.commit()
    db.refresh(usuario)
    return usuario

@app.patch("/usuarios/{usuario_id}/premium", response_model=Usuario)
def hacer_premium(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.premium = True
    db.commit()
    db.refresh(usuario)
    return usuario

@app.get("/usuarios/inactivos/", response_model=List[Usuario])
def usuarios_inactivos(db: Session = Depends(get_db)):
    return db.query(models.Usuario).filter(models.Usuario.activo == False).all()

@app.get("/usuarios/premium-inactivos/", response_model=List[Usuario])
def usuarios_premium_inactivos(db: Session = Depends(get_db)):
    return db.query(models.Usuario).filter(
        models.Usuario.premium == True, 
        models.Usuario.activo == False
    ).all()

# Endpoints de Tareas (CRUD completo)
@app.post("/tareas/", response_model=Tarea)
def crear_tarea(tarea: TareaBase, db: Session = Depends(get_db)):
    try:
        db_tarea = models.Tarea(**tarea.dict())
        db.add(db_tarea)
        db.commit()
        db.refresh(db_tarea)
        return db_tarea
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear tarea: {str(e)}")
        raise HTTPException(status_code=400, detail="Error al crear tarea")

@app.get("/tareas/", response_model=List[Tarea])
def leer_tareas(db: Session = Depends(get_db)):
    return db.query(models.Tarea).all()

@app.get("/tareas/{tarea_id}", response_model=Tarea)
def leer_tarea(tarea_id: int, db: Session = Depends(get_db)):
    tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

@app.patch("/tareas/{tarea_id}/completar", response_model=Tarea)
def completar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    tarea.completada = True
    db.commit()
    db.refresh(tarea)
    return tarea

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)