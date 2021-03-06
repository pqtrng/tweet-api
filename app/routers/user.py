from fastapi import status, HTTPException, APIRouter
from fastapi_sqlalchemy import db

# Local
from .. import models, schemas, utils


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.session.add(new_user)
    db.session.commit()
    db.session.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.User)
def get_user(id: int):
    user = db.session.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} was not found.",
        )

    return user
