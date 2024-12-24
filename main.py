from db import db
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from config import config
import uvicorn
from loguru import logger
from views import api as user_api, post_api


def init_app() -> FastAPI:
    """
    Initialize the FastAPI application with routes, database connections,
    and event handlers.
    """
    app = FastAPI(
        title="Users and Posts App",
        description="API for managing users and posts.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    @app.on_event("startup")
    async def startup():
        """
        Startup event to initialize database connection and log startup.
        """
        try:
            logger.info("Starting application...")
            db.connect(config.DB_CONFIG)
            logger.info("Database connection established.")
        except Exception as e:
            logger.error(f"Failed to connect to the database: {e}")
            raise

    @app.on_event("shutdown")
    async def shutdown():
        """
        Shutdown event to clean up resources like the database connection.
        """
        try:
            logger.info("Shutting down application...")
            await db.disconnect()
            logger.info("Database connection closed.")
        except Exception as e:
            logger.error(f"Failed to disconnect from the database: {e}")

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """
        Global exception handler to capture and log unexpected errors.
        """
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

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
