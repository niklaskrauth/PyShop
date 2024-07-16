import json

from concurrent.futures import ThreadPoolExecutor

from http import HTTPStatus

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.database.db_connection import close_connection, create_connection
from app.handlers.article_handler import ArticleHandler
from app.services.articles_service import ArticlesService
from app.models.dto.article_model_dto import ArticleModelDTO, ArticlesModelDTO, ArticleModelDTOEndpoint

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app = FastAPI(title="PyShop API", description="This is a very fancy project", version="0.3.1", openapi_prefix="/api")
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


@app.get("/health",
         name="Health Check",
         description="Check the health of the backend",
         responses={200: {"description": "Backend is healthy", "model": str}})
async def health_endpoint() -> str:
    return "Backend is healthy"


@app.get("/articles",
         name="Get all articles",
         description="Get all articles from the database",
         responses={200: {"model": ArticlesModelDTO},
                    404: {"description": "Articles not found", "model": str},
                    500: {"description": "Internal Server Error", "model": str}
                    })
async def get_articles_endpoint() -> JSONResponse:
    response = article_handler.get_articles_handler()

    if isinstance(response, ArticlesModelDTO):
        return JSONResponse(status_code=200, content=json.loads(response.model_dump_json()))
    elif hasattr(response, 'status_code') and response.status_code == 404:
        return JSONResponse(status_code=404, content={"message": "Articles not found"})
    else:
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})


@app.get("/article/{id}",
         name="Get an article",
         description="Get a specific article from the database",
         responses={200: {"model": ArticleModelDTO},
                    404: {"description": "Article not found", "model": str},
                    422: {"description": "Unprocessable Entity", "model": str},
                    500: {"description": "Internal Server Error", "model": str}
                    })
async def get_article_endpoint(id: int) -> JSONResponse:
    response = article_handler.get_article_handler(id)

    if isinstance(response, ArticleModelDTO):
        return JSONResponse(status_code=200, content=json.loads(response.model_dump_json()))
    elif hasattr(response, 'status_code') and response.status_code == 404:
        return JSONResponse(status_code=404, content={"message": "Article not found"})
    else:
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})


@app.post("/article",
          name="Create an article",
          description="Create an article and add it to the database",
          responses={200: {"description": "Article created successfully!", "model": ArticleModelDTOEndpoint},
                     400: {"description": "Bad Request", "model": str},
                     422: {"description": "Unprocessable Entity", "model": str},
                     500: {"description": "Internal Server Error", "model": str}
                     })
async def create_article_endpoint(article: ArticleModelDTOEndpoint) -> JSONResponse:
    future = executor.submit(article_handler.create_article_handler, article)
    response = future.result()

    if isinstance(response, ArticleModelDTOEndpoint):
        return JSONResponse(status_code=200, content=json.loads(response.model_dump_json()))
    elif hasattr(response, 'status_code') and response.status_code == 400:
        return JSONResponse(status_code=400, content={"message": "Bad Request"})
    else:
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})


@app.put("/article/{id}",
         name="Update an article",
         description="Update an article in the database",
         responses={200: {"description": "Article updated successfully!", "model": ArticleModelDTOEndpoint},
                    400: {"description": "Bad Request", "model": str},
                    422: {"description": "Unprocessable Entity", "model": str},
                    500: {"description": "Internal Server Error", "model": str}
                    })
async def update_article_endpoint(id: int, article: ArticleModelDTOEndpoint) -> JSONResponse:
    response = article_handler.update_article_handler(id, article)

    if isinstance(response, ArticleModelDTOEndpoint):
        return JSONResponse(status_code=200, content=json.loads(response.model_dump_json()))
    elif hasattr(response, 'status_code') and response.status_code == 400:
        return JSONResponse(status_code=400, content={"message": "Bad Request"})
    else:
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})


@app.delete("/article/{id}",
            name="Delete an article",
            description="Delete an article from the database",
            responses={200: {"description": "Article deleted successfully!", "model": str},
                       404: {"description": "Article not found", "model": str},
                       422: {"description": "Unprocessable Entity", "model": str},
                       500: {"description": "Internal Server Error", "model": str}
                       })
async def delete_article_endpoint(id: int) -> JSONResponse:
    response = article_handler.delete_article_handler(id)

    if response is None:
        return JSONResponse(status_code=200, content={"message": "Article deleted successfully!"})
    elif hasattr(response, 'status_code') and response.status_code == 404:
        return JSONResponse(status_code=404, content={"message": "Article not found"})
    else:
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})


@app.get("/close-connection",
         name="Close connection",
         description="Close the database connection",
         responses={200: {"description": "Connection closed successfully!", "model": HTTPStatus}})
async def close_endpoint() -> HTTPStatus:
    close_connection(connection)
    return HTTPStatus.OK
