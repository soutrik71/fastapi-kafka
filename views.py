from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from models import User, Post
from db import db


class UserSchema(BaseModel):
    full_name: str


class UserSerializer(BaseModel):
    id: str
    full_name: str

    class Config:
        from_attributes = True


class PostSchema(BaseModel):
    user_id: str
    data: str


class PostSerializer(BaseModel):
    id: str
    user_id: str
    data: str

    class Config:
        from_attributes = True


user_api = APIRouter(
    prefix="/users",
)

post_api = APIRouter(
    prefix="/posts",
)


@api.post("/")
async def create_user(
    user: UserSchema, db_session=Depends(db.get_db)
) -> UserSerializer:
    user = await User.create(db_session, **user.dict())
    return user


@api.get("/{id}")
async def get_user(id: str, db_session=Depends(db.get_db)) -> UserSerializer:
    user = await User.get(db_session, id)
    return user


@api.get("/")
async def get_all_users(db_session=Depends(db.get_db)) -> List[UserSerializer]:
    users = await User.get_all(db_session)
    return users


@api.put("/{id}")
async def update(
    id: str, user: UserSchema, db_session=Depends(db.get_db)
) -> UserSerializer:
    user = await User.update(db_session, id, **user.dict())
    return user


@api.delete("/{id}")
async def delete_user(id: str, db_session=Depends(db.get_db)) -> bool:
    return await User.delete(db_session, id)


@post_api.post("/")
async def create_post(
    post: PostSchema, db_session=Depends(db.get_db)
) -> PostSerializer:
    post = await Post.create(db_session, **post.dict())
    return post


@post_api.get("/{id}")
async def get_post(id: str, db_session=Depends(db.get_db)) -> PostSerializer:
    post = await Post.get(db_session, id)
    return post


@post_api.get("/")
async def get_all_posts(db_session=Depends(db.get_db)) -> List[PostSerializer]:
    posts = await Post.get_all(db_session)
    return posts


@post_api.put("/{id}")
async def update_post(
    id: str, post: PostSchema, db_session=Depends(db.get_db)
) -> PostSerializer:
    post = await Post.update(db_session, id, **post.dict())
    return post


@post_api.delete("/{id}")
async def delete_post(id: str, db_session=Depends(db.get_db)) -> bool:
    return await Post.delete(db_session, id)
