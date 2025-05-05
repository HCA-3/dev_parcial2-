from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    estado = Column(String, default="Activo")  # Activo, Inactivo
    tipo = Column(String, default="Regular")  # Regular, Premium
