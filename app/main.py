import sys
from concurrent.futures import ThreadPoolExecutor

from http import HTTPStatus

from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.database.db_connection import close_connection, create_connection
from app.handlers.article_handler import ArticleHandler
from app.models.error.error_model import ErrorResponseModel
from app.services.articles_service import ArticlesService
from app.models.dto.article_model_dto import (
    ArticleModelDTO,
    ArticlesModelDTO,
    ArticleModelDTOEndpoint,
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

logger.add(
    sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
)
app = FastAPI(
    title="PyShop API",
    description="This is a very fancy project",
    version="0.3.1",
    openapi_prefix="/api",
)
connection = create_connection()
cursor = connection.cursor()
article_service = ArticlesService(connection)
article_handler = ArticleHandler(article_service)
executor = ThreadPoolExecutor(max_workers=2)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Fix up the get_article-service                                  -> DONE

# TODO: Difference uvicorn gunicorn?                                    -> DONE
# Gunicorn is a WSGI HTTP server for Python web applications. The Gunicorn server is broadly compatible with various web frameworks, simply implemented, light on server resources, and fairly speedy.
# Uvicorn is a lightning-fast ASGI server implementation that is perfect for running asynchronous web applications.
# Guvicorn: Gunicorn + Uvicorn. It is a Gunicorn worker class that runs an ASGI application, using Uvicorn to serve the application.
# TODO: Read about workers and how to be used with uvicorn/gunicorn     -> DONE
# A worker is a separate process that is responsible for handling requests.
# Gunicorn uses workers to handle requests and runs parallel instances of the application.
# Uvicorn is an ASGI server that can run multiple worker processes. Although it is not recommended to run multiple worker processes with Uvicorn, it is possible to do so.
# TODO: Understand poetry                                               -> DONE
# Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you.
# TODO. Understand the Python environment (venv)                        -> DONE
# A virtual environment is an isolated directory that contains a Python Project for a particular version of Python, plus a number of additional packages.
# TODO: Why the environment is needed?                                  -> DONE
# So that the dependencies of the project are isolated from the system dependencies. This way, the project can be run on any machine without having to worry about the dependencies.


@app.get(
    "/health",
    name="Health Check",
    description="Check the health of the backend",
    responses={200: {"description": "Backend is healthy", "model": str}},
)
async def health_endpoint() -> str:
    return "Backend is healthy"


@app.get(
    "/articles",
    name="Get all articles",
    description="Get all articles from the database",
    responses={
        200: {"model": ArticlesModelDTO},
        404: {"description": "Articles not found", "model": ErrorResponseModel},
        500: {"description": "Internal Server Error", "model": ErrorResponseModel},
    },
)
async def get_articles_endpoint() -> JSONResponse:
    return article_handler.get_articles_handler()


@app.get(
    "/article/{id}",
    name="Get an article",
    description="Get a specific article from the database",
    responses={
        200: {"model": ArticleModelDTO},
        404: {"description": "Article not found", "model": ErrorResponseModel},
        422: {"description": "Unprocessable Entity", "model": ErrorResponseModel},
        500: {"description": "Internal Server Error", "model": ErrorResponseModel},
    },
)
async def get_article_endpoint(id: int) -> JSONResponse:
    return article_handler.get_article_handler(id)


@app.post(
    "/article",
    name="Create an article",
    description="Create an article and add it to the database",
    responses={
        200: {
            "description": "Article created successfully!",
            "model": ArticleModelDTOEndpoint,
        },
        400: {"description": "Bad Request", "model": ErrorResponseModel},
        422: {"description": "Unprocessable Entity", "model": ErrorResponseModel},
        500: {"description": "Internal Server Error", "model": ErrorResponseModel},
    },
)
async def create_article_endpoint(article: ArticleModelDTOEndpoint) -> JSONResponse:
    future = executor.submit(article_handler.create_article_handler, article)
    return future.result()


@app.put(
    "/article/{id}",
    name="Update an article",
    description="Update an article in the database",
    responses={
        200: {
            "description": "Article updated successfully!",
            "model": ArticleModelDTOEndpoint,
        },
        400: {"description": "Bad Request", "model": ErrorResponseModel},
        422: {"description": "Unprocessable Entity", "model": ErrorResponseModel},
        500: {"description": "Internal Server Error", "model": ErrorResponseModel},
    },
)
async def update_article_endpoint(
    id: int, article: ArticleModelDTOEndpoint
) -> JSONResponse:
    return article_handler.update_article_handler(id, article)


@app.delete(
    "/article/{id}",
    name="Delete an article",
    description="Delete an article from the database",
    responses={
        200: {
            "description": "Article deleted successfully!",
            "model": ErrorResponseModel,
        },
        404: {"description": "Article not found", "model": ErrorResponseModel},
        422: {"description": "Unprocessable Entity", "model": ErrorResponseModel},
        500: {"description": "Internal Server Error", "model": ErrorResponseModel},
    },
)
async def delete_article_endpoint(id: int) -> JSONResponse:
    return article_handler.delete_article_handler(id)


@app.get(
    "/close-connection",
    name="Close connection",
    description="Close the database connection",
    responses={
        200: {"description": "Connection closed successfully!", "model": HTTPStatus}
    },
)
async def close_endpoint() -> HTTPStatus:
    close_connection(connection)
    return HTTPStatus.OK
