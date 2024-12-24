from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Column,
    DateTime,
    String,
    Integer,
    ForeignKey,
)
from sqlalchemy.sql import expression as sql
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    full_name = Column(String, nullable=False, index=True)
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )

    posts = relationship("Post", back_populates="user", cascade="all, delete")

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"full_name={self.full_name}, "
            f")>"
        )

    # CRUD operations
    @classmethod
    async def create(cls, db, **kwargs) -> "User":
        query = (
            sql.insert(cls)
            .values(id=str(uuid4()), **kwargs)
            .returning(cls.id, cls.full_name)
        )
        users = await db.execute(query)
        await db.commit()
        return users.first()

    @classmethod
    async def update(cls, db, id, **kwargs) -> "User":
        query = (
            sql.update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
            .returning(cls.id, cls.full_name)
        )
        users = await db.execute(query)
        await db.commit()
        return users.first()

    @classmethod
    async def get(cls, db, id) -> "User":
        query = sql.select(cls).where(cls.id == id)
        users = await db.execute(query)
        (user,) = users.first()
        return user

    @classmethod
    async def get_all(cls, db) -> list["User"]:
        query = sql.select(cls)
        users = await db.execute(query)
        users = users.scalars().all()
        return users

    @classmethod
    async def delete(cls, db, id) -> bool:
        query = (
            sql.delete(cls)
            .where(cls.id == id)
            .returning(
                cls.id,
                cls.full_name,
            )
        )
        await db.execute(query)
        await db.commit()
        return True


class Post(Base):
    __tablename__ = "posts"
    id = Column(
        String, primary_key=True, default=lambda: str(uuid4())
    )  # Use UUID for ID
    user_id = Column(ForeignKey("users.id"), nullable=False)
    data = Column(String, nullable=False)

    user = relationship("User", back_populates="posts")

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"data={self.data}, "
            f"user_id={self.user_id}"
            f")>"
        )

    @classmethod
    async def create(cls, db, user_id: str, **kwargs) -> "Post":
        """
        Create a Post record after validating that the user exists.

        Args:
            db: Database session.
            user_id: ID of the user associated with the post.
            **kwargs: Other fields for the Post model.

        Returns:
            The created Post object.
        """
        # Validate that the user exists
        try:
            user_query = sql.select(User).where(User.id == user_id)
            result = await db.execute(user_query)
            user = result.scalar_one()  # Ensure exactly one result is returned
        except NoResultFound:
            raise ValueError(f"User with id {user_id} does not exist.")

        # Create the post
        post_id = str(uuid4())
        query = (
            sql.insert(cls)
            .values(id=post_id, user_id=user_id, **kwargs)
            .returning(cls.id, cls.data, cls.user_id)
        )
        post_result = await db.execute(query)
        await db.commit()

        return post_result.first()

    @classmethod
    async def update(cls, db, id, **kwargs) -> "Post":
        query = (
            sql.update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
            .returning(cls.id, cls.data, cls.user_id)
        )
        post = await db.execute(query)
        await db.commit()
        return post.first()

    @classmethod
    async def get(cls, db, id) -> "Post":
        query = sql.select(cls).where(cls.id == id)
        posts = await db.execute(query)
        (post,) = posts.first()
        return post

    @classmethod
    async def get_all(cls, db) -> list["Post"]:
        query = sql.select(cls)
        posts = await db.execute(query)
        posts = posts.scalars().all()
        return posts

    @classmethod
    async def delete(cls, db, id) -> bool:
        query = (
            sql.delete(cls)
            .where(cls.id == id)
            .returning(
                cls.id,
                cls.data,
                cls.user_id,
            )
        )
        await db.execute(query)
        await db.commit()
        return True
