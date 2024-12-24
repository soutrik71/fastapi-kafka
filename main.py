from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from loguru import logger
from config import config
from db import db
from views import user_api, post_api


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Starting application...")
        db.connect(config.DB_CONFIG)
        logger.info("Database connection established.")
        yield
    except Exception as e:
        logger.error(f"Failed during startup: {e}")
        raise
    finally:
        try:
            await db.disconnect()
            logger.info("Database connection closed.")
        except Exception as e:
            logger.error(f"Failed during shutdown: {e}")


def init_app() -> FastAPI:
    app = FastAPI(
        title="Users and Posts App",
        description="API for managing users and posts.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred."},
        )

    # Include user routes
    app.include_router(
        user_api,
        prefix="/api/user",
        tags=["Users"],
    )

    # Include post routes
    app.include_router(
        post_api,
        prefix="/api/post",
        tags=["Posts"],
    )

    return app


app = init_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
