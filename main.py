.from contextlib import asynccontextmanager
from fastapi import FastAPI
from utils.connection_db import init_db


@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    yield
app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
