from http import HTTPStatus

from app.models.dao.article_model_dao import ArticleModelDAO, ArticlesModelDAO
from app.models.dto.article_model_dto import ArticlesModelDTO, ArticleModelDTO, ArticleModelDTOEndpoint
from app.util.converter import convert_articles_model_dao_to_articles_model_dto, convert_list_to_article_model_dto, \
    convert_article_model_dto_endpoint_to_article_model_dao


class ArticleHandler:
    def __init__(self, service):
        self.service = service

    def get_articles_handler(self) -> ArticlesModelDTO | HTTPStatus:
        try:
            articles: ArticlesModelDAO = self.service.get_all_articles()
            if articles is not None:
                articles: ArticlesModelDTO = convert_articles_model_dao_to_articles_model_dto(articles)
                return articles
            return HTTPStatus.NOT_FOUND
        except Exception:
            return HTTPStatus.INTERNAL_SERVER_ERROR

    def get_article_handler(self, id: int) -> ArticleModelDTO | HTTPStatus:
        try:
            article: list = self.service.get_article(id)
            if article is not None:
                article: ArticleModelDTO = convert_list_to_article_model_dto(article)
                return article
            return HTTPStatus.NOT_FOUND
        except Exception:
            return HTTPStatus.INTERNAL_SERVER_ERROR

    def create_article_handler(self, article: ArticleModelDTOEndpoint) -> (
            ArticleModelDTOEndpoint | HTTPStatus):
        try:
            if (article.first_name is not None and
                    article.last_name is not None and
                    article.price is not None):
                self.service.create_article(convert_article_model_dto_endpoint_to_article_model_dao(article))
                return article
            return HTTPStatus.UNPROCESSABLE_ENTITY
        except Exception:
            return HTTPStatus.INTERNAL_SERVER_ERROR

    def update_article_handler(self, id: int, article: ArticleModelDTOEndpoint) -> (
            ArticleModelDAO | HTTPStatus):
        try:
            if (article.first_name is not None and
                    article.last_name is not None and
                    article.price is not None):
                article = convert_article_model_dto_endpoint_to_article_model_dao(article)
                self.service.update_article(id, article)
                return article
            return HTTPStatus.UNPROCESSABLE_ENTITY
        except Exception:
            return HTTPStatus.INTERNAL_SERVER_ERROR

    def delete_article_handler(self, id: int) -> HTTPStatus:
        try:
            if self.service.exists_article_with_id(id):
                self.service.delete_article(id)
                return HTTPStatus.OK
            return HTTPStatus.NOT_FOUND
        except Exception:
            return HTTPStatus.INTERNAL_SERVER_ERROR
