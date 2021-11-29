from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi_sqlalchemy import db

from .. import schemas, utils, models, oauth2

router = APIRouter(tags=["Authentication"], prefix="/login")


@router.post("", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    user = (
        db.session.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials."
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials."
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
