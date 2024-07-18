import json

from loguru import logger
from starlette.responses import JSONResponse

from app.models.dao.article_model_dao import ArticlesModelDAO, ArticleModelDAO
from app.models.dto.article_model_dto import (
    ArticlesModelDTO,
    ArticleModelDTO,
    ArticleModelDTOEndpoint,
)
from app.util.converter import (
    convert_articles_model_dao_to_articles_model_dto,
    convert_article_model_dto_endpoint_to_article_model_dao,
    convert_article_model_dao_to_article_model_dto,
)


class ArticleHandler:
    def __init__(self, service):
        self.service = service

    def get_articles_handler(self) -> JSONResponse:
        try:
            articles: ArticlesModelDAO = self.service.get_all_articles()

            if articles is not None and len(articles) > 0:
                articles: ArticlesModelDTO = (
                    convert_articles_model_dao_to_articles_model_dto(articles)
                )
                return JSONResponse(
                    content=json.loads(articles.model_dump_json()), status_code=200
                )

            logger.warning("No articles found")
            return JSONResponse(
                content={"message": "No articles found"}, status_code=404
            )

        except Exception as e:
            logger.error(f"An error occurred while retrieving articles: {e}")
            return JSONResponse(
                content={"message": "Internal Server Error"}, status_code=500
            )

    def get_article_handler(self, id: int) -> JSONResponse:
        try:
            article: ArticleModelDAO = self.service.get_article(id)
            if article is not None:
                article: ArticleModelDTO = (
                    convert_article_model_dao_to_article_model_dto(article)
                )
                return JSONResponse(
                    content=json.loads(article.model_dump_json()), status_code=200
                )

            logger.warning("Article not found")
            return JSONResponse(
                content={"message": "Article not found"}, status_code=404
            )

        except Exception as e:
            logger.error(f"An error occurred while retrieving article: {e}")
            return JSONResponse(
                content={"message": "Internal Server Error"}, status_code=500
            )

    def create_article_handler(self, article: ArticleModelDTOEndpoint) -> JSONResponse:
        try:
            if (
                article.first_name is not None
                and article.last_name is not None
                and article.price is not None
            ):
                self.service.create_article(
                    convert_article_model_dto_endpoint_to_article_model_dao(article)
                )
                return JSONResponse(
                    content=json.loads(article.model_dump_json()), status_code=200
                )

            logger.warning("Bad Request")
            return JSONResponse(content={"message": "Bad Request"}, status_code=400)

        except Exception as e:
            logger.error(f"An error occurred while creating article: {e}")
            return JSONResponse(
                content={"message": "Internal Server Error"}, status_code=500
            )

    def update_article_handler(
        self, id: int, article: ArticleModelDTOEndpoint
    ) -> JSONResponse:
        try:
            if (
                article.first_name is not None
                and article.last_name is not None
                and article.price is not None
            ):
                self.service.update_article(
                    id, convert_article_model_dto_endpoint_to_article_model_dao(article)
                )
                return JSONResponse(
                    content=json.loads(article.model_dump_json()), status_code=200
                )

            logger.warning("Bad Request")
            return JSONResponse(content={"message": "Bad Request"}, status_code=400)

        except Exception as e:
            logger.error(f"An error occurred while updating article: {e}")
            return JSONResponse(
                content={"message": "Internal Server Error"}, status_code=500
            )

    def delete_article_handler(self, id: int) -> JSONResponse:
        try:
            if self.service.exists_article_with_id(id):
                self.service.delete_article(id)
                return JSONResponse(
                    content={"message": "Article deleted successfully!"},
                    status_code=200,
                )

            return JSONResponse(
                content={"message": "Article not found"}, status_code=404
            )

        except Exception as e:
            logger.error(f"An error occurred while deleting article: {e}")
            return JSONResponse(
                content={"message": "Internal Server Error"}, status_code=500
            )
