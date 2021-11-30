from jose import jwt
from app.config import settings
from app import schemas
import pytest


def test_create_user(client):
    res = client.post(
        "/users", json={"email": "hello123@gmail.com", "password": "password123"}
    )
    new_user = schemas.User(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201
