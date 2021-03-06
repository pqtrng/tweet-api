from fastapi import Response, status, HTTPException, APIRouter, Depends
from fastapi_sqlalchemy import db
from typing import List, Optional

from .. import models, schemas, oauth2

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


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=schemas.TweetCreate
)
def create_tweet(
    tweet: schemas.TweetCreate,
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    new_tweet = models.Tweet(owner_id=current_user.id, **tweet.dict())
    db.session.add(new_tweet)
    db.session.commit()
    db.session.refresh(new_tweet)
    return new_tweet


@router.put("/{id}", response_model=schemas.TweetCreate)
def update_tweet(
    id: int,
    tweet: schemas.TweetCreate,
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    tweet_query = db.session.query(models.Tweet).filter(models.Tweet.id == id)

    # Check if the tweet exist
    if not tweet_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist.",
        )

    # Check if the current user is the owner
    if tweet_query.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action.",
        )

    # Execute the action
    tweet_query.update(values=tweet.dict(), synchronize_session=False)
    db.session.commit()

    return tweet_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tweet(
    id: int, current_user: schemas.User = Depends(oauth2.get_current_user)
):
    tweet_query = db.session.query(models.Tweet).filter(models.Tweet.id == id)

    # Check if the tweet exist
    if not tweet_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tweet with id: {id} does not exist.",
        )

    # Check if the current user is the owner
    if tweet_query.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action.",
        )

    # Execute the action
    tweet_query.delete(synchronize_session=False)
    db.session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
