from fastapi import FastAPI
from .routers import tweet, user, auth

from . import models, database

# Connect to database
models.Base.metadata.create_all(bind=database.engine)

# App
app = FastAPI()


# Middleware


# Routes
app.include_router(tweet.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Homepage."}
