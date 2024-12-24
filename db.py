from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config import config

Base = declarative_base()


class Database:
    def __init__(self):
        self._engine = None
        self._session = None

    def connect(self, db_config: str = config.DB_CONFIG) -> None:
        """
        Establish a connection to the database and initialize the session factory.
        """
        if not db_config:
            raise ValueError("Database configuration URL is required")

        logger.info("Initializing database connection...")
        self._engine = create_async_engine(
            db_config, future=True, echo=True  # Enable SQLAlchemy debug logs
        )

        self._session = async_sessionmaker(
            bind=self._engine, class_=AsyncSession, expire_on_commit=False
        )
        logger.info("Database connection initialized.")

    async def disconnect(self) -> None:
        """
        Dispose of the database connection.
        """
        if self._engine:
            logger.info("Disposing database engine...")
            await self._engine.dispose()
            logger.info("Database engine disposed.")

    async def get_db(self):
        """
        Provide a database session for dependency injection.
        """
        if not self._session:
            raise RuntimeError(
                "Database sessionmaker is not initialized. Call 'connect' first."
            )

        async with self._session() as session:
            try:
                yield session
            except Exception as e:
                logger.error(f"Error during database session: {e}")
                raise
            finally:
                await session.close()
                logger.info("Database session closed.")


# Initialize the database instance
db = Database()

if __name__ == "__main__":
    import asyncio

    async def main():
        try:
            logger.info("Starting database operations...")
            db.connect()
            logger.info("Connected to the database.")
            await db.disconnect()
            logger.info("Disconnected from the database.")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    asyncio.run(main())
