from fastapi import FastAPI
from . import models
from .database import engine
from .routers import tweet

# Connect to database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tweet.router)


@app.get("/")
def root():
    return {"message": "Hello, World."}
