from fastapi import FastAPI
from .routers import tweet, user, auth

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
