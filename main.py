from fastapi import FastAPI
from .database import Base, engine
from .routes import usuarios, tareas

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(tareas.router, prefix="/tareas", tags=["Tareas"])
