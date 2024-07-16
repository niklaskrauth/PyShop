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

# TODO: Add tests via Pytest

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
