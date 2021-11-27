from fastapi import FastAPI
from .routers import tweet
from fastapi_sqlalchemy import DBSessionMiddleware
from .config import settings

# App
app = FastAPI()


# Middleware
app.add_middleware(DBSessionMiddleware, db_url=settings.get_url())


# Routes
app.include_router(tweet.router)


@app.get("/")
def root():
    return {"message": "Homepage."}
