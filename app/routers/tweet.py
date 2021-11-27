from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi_sqlalchemy import db

from sqlalchemy.orm import Session
from sqlalchemy import func

from typing import List, Optional
from .. import models, schemas

router = APIRouter(prefix="/tweets", tags=["Tweets"])


@router.get("", response_model=List[schemas.TweetBase])
def get_tweets(
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    tweets = (
        db.session.query(models.Tweet)
        .group_by(models.Tweet.id)
        .filter(models.Tweet.title.contains(search))
        .limit(limit=limit)
        .offset(offset=skip)
        .all()
    )

    return tweets


@router.get("/{id}", response_model=schemas.TweetBase)
def get_tweets(id: int):
    tweet = db.session.query(models.Tweet).filter(models.Tweet.id == id).first()
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tweet with id: {id} was not found.",
        )
    print(tweet)
    return tweet
