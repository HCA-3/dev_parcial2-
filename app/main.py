from fastapi import FastAPI
from app.database import engine
from app import models
from routes.usuarios import router as usuarios_router
from routes.tareas import router as tareas_router
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(usuarios_router)
app.include_router(tareas_router)

# Para desarrollo local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))