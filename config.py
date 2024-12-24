import os
from dotenv import load_dotenv, find_dotenv
from loguru import logger

load_dotenv(find_dotenv(".env"))


class Config:
    POSTGRES_USER = os.getenv("POSTGRES_USER", "POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "POSTGRES_DB")
    DB_HOST = os.getenv("DB_HOST", "DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "DB_PORT")
    DB_CONFIG = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"


config = Config()

if __name__ == "__main__":
    logger.info(config.DB_CONFIG)
