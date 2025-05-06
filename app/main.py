from fastapi import FastAPI
import os
from app.database import engine
from app import models
from routes.usuarios import router as usuarios_router
from routes.tareas import router as tareas_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(usuarios_router)
app.include_router(tareas_router)

# Especial para Render
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=True
    )