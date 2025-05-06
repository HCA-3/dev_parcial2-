from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), index=True)
    email = Column(String(100), unique=True, index=True)
    activo = Column(Boolean, default=True)
    premium = Column(Boolean, default=False)
    
    # Relación con tareas
    tareas = relationship("Tarea", back_populates="usuario")

class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), index=True)
    descripcion = Column(String(255))
    completada = Column(Boolean, default=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    
    # Relación con usuario
    usuario = relationship("Usuario", back_populates="tareas")