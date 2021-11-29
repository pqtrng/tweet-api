from fastapi import FastAPI
from .routers import tweet, user, auth
from fastapi_sqlalchemy import DBSessionMiddleware
from .config import settings

# App
app = FastAPI()


# Middleware
app.add_middleware(DBSessionMiddleware, db_url=settings.get_url())


# Routes
app.include_router(tweet.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Homepage."}
