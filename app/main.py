from fastapi import FastAPI
from . import models
from .database import engine

# Connect to database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello, World."}
