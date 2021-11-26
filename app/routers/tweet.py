from fastapi import Response, status, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session
from sqlalchemy import func

from typing import List, Optional

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/tweets", tags=["Tweets"])


@router.get("", response_model=List[schemas.TweetBase])
def get_tweets(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    tweets = (
        db.query(models.Tweet)
        .group_by(models.Tweet.id)
        .filter(models.Tweet.title.contains(search))
        .limit(limit=limit)
        .offset(offset=skip)
        .all()
    )

    return tweets
