from pydantic import BaseModel
from typing import Optional, List

class TareaBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    completado: bool = False

class TareaCreate(TareaBase):
    pass

class Tarea(TareaBase):
    id: int
    usuario_id: int

    class Config:
        orm_mode = True

class UsuarioBase(BaseModel):
    nombre: str
    email: str
    tipo: Optional[str] = "No Premium"
    estado: Optional[str] = "Active"

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id: int
    tareas: List[Tarea] = []

    class Config:
        orm_mode = True