from fastapi import FastAPI
from app.database import engine
from app import models
from routes.usuarios import router as usuarios_router
from routes.tareas import router as tareas_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(usuarios_router)
app.include_router(tareas_router)