from contextlib import asynccontextmanager
from fastapi import FastAPI
from controllers.RoutinesGeneratorController import router
from factories.PostgresConnectionFactory import PostgresConnectionFactory
import uvicorn
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for application startup and shutdown.
    This replaces the deprecated @app.on_event methods.
    """
    # Initialize necessary resources on startup
    connection_factory = PostgresConnectionFactory()
    connection_factory.initialize_database()
    print("Database initialized successfully.")

    # Yield control back to the app
    yield

    # Perform cleanup tasks on shutdown (if needed)
    print("Application is shutting down.")


# Set up the FastAPI app with the lifespan context manager
app = FastAPI(lifespan=lifespan)

# Include the controller endpoints
app.include_router(router)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
