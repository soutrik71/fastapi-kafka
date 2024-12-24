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


# Define API routers
user_api = APIRouter(
    prefix="/users",
)

post_api = APIRouter(
    prefix="/posts",
)


# Define API routes for users and posts with CRUD operations using the models and database instance


@user_api.post(
    "/",
    description="Create a new user",
    response_model=UserSerializer,
    status_code=201,
    tags=["Users"],
)
async def create_user(
    user: UserSchema, db_session=Depends(db.get_db)
) -> UserSerializer:
    """Create a new user"""
    user = await User.create(db_session, **user.dict())
    return user


@user_api.get(
    "/{id}",
    response_model=UserSerializer,
    tags=["Users"],
    status_code=200,
    description="Get a user by ID",
)
async def get_user(id: str, db_session=Depends(db.get_db)) -> UserSerializer:
    """Get a user by ID"""
    user = await User.get(db_session, id)
    return user


@user_api.get(
    "/",
    response_model=List[UserSerializer],
    tags=["Users"],
    status_code=200,
    description="Get all users",
)
async def get_all_users(db_session=Depends(db.get_db)) -> List[UserSerializer]:
    """Get all users"""
    users = await User.get_all(db_session)
    return users


@user_api.put(
    "/{id}",
    response_model=UserSerializer,
    tags=["Users"],
    status_code=200,
    description="Update a user by ID",
)
async def update(
    id: str, user: UserSchema, db_session=Depends(db.get_db)
) -> UserSerializer:
    """Update a user by ID"""
    user = await User.update(db_session, id, **user.dict())
    return user


@user_api.delete(
    "/{id}",
    response_model=bool,
    tags=["Users"],
    status_code=200,
    description="Delete a user by ID",
)
async def delete_user(id: str, db_session=Depends(db.get_db)) -> bool:
    """Delete a user by ID"""
    return await User.delete(db_session, id)


@post_api.post(
    "/",
    response_model=PostSerializer,
    status_code=201,
    tags=["Posts"],
    description="Create a new post",
)
async def create_post(
    post: PostSchema, db_session=Depends(db.get_db)
) -> PostSerializer:
    post = await Post.create(db_session, **post.dict())
    return post


@post_api.get(
    "/{id}",
    response_model=PostSerializer,
    tags=["Posts"],
    status_code=200,
    description="Get a post by ID",
)
async def get_post(id: str, db_session=Depends(db.get_db)) -> PostSerializer:
    post = await Post.get(db_session, id)
    return post


@post_api.get(
    "/",
    response_model=List[PostSerializer],
    tags=["Posts"],
    status_code=200,
    description="Get all posts",
)
async def get_all_posts(db_session=Depends(db.get_db)) -> List[PostSerializer]:
    posts = await Post.get_all(db_session)
    return posts


@post_api.put(
    "/{id}",
    response_model=PostSerializer,
    tags=["Posts"],
    status_code=200,
    description="Update a post by ID",
)
async def update_post(
    id: str, post: PostSchema, db_session=Depends(db.get_db)
) -> PostSerializer:
    post = await Post.update(db_session, id, **post.dict())
    return post


@post_api.delete(
    "/{id}",
    response_model=bool,
    tags=["Posts"],
    status_code=200,
    description="Delete a post by ID",
)
async def delete_post(id: str, db_session=Depends(db.get_db)) -> bool:
    return await Post.delete(db_session, id)
