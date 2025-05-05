from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nombre: str
    estado: str = "Activo"
    tipo: str = "Regular"

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    estado: str
    tipo: str

class UsuarioOut(UsuarioBase):
    id: int

    class Config:
        orm_mode = True
