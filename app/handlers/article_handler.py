from app.errors.custom_error import CustomError
from app.models.dao.article_model_dao import ArticlesModelDAO
from app.models.dto.article_model_dto import ArticlesModelDTO, ArticleModelDTO, ArticleModelDTOEndpoint
from app.util.converter import convert_articles_model_dao_to_articles_model_dto, convert_list_to_article_model_dto, \
    convert_article_model_dto_endpoint_to_article_model_dao


class ArticleHandler:
    def __init__(self, service):
        self.service = service

    def get_articles_handler(self) -> ArticlesModelDTO | CustomError:
        try:
            articles: ArticlesModelDAO = self.service.get_all_articles()
            if articles is not None and len(articles) > 0:
                articles: ArticlesModelDTO = convert_articles_model_dao_to_articles_model_dto(articles)
                return articles
            return CustomError("Error getting all articles", 404)
        except Exception:
            return CustomError("Internal Error", 500)

    def get_article_handler(self, id: int) -> ArticleModelDTO | CustomError:
        try:
            article: list = self.service.get_article(id)
            if article is not None:
                article: ArticleModelDTO = convert_list_to_article_model_dto(article)
                return article
            return CustomError("Error getting article", 404)
        except Exception:
            return CustomError("Internal Error", 500)

    def create_article_handler(self, article: ArticleModelDTOEndpoint) -> ArticleModelDTOEndpoint | CustomError:
        try:
            if (article.first_name is not None and
                    article.last_name is not None and
                    article.price is not None):
                self.service.create_article(convert_article_model_dto_endpoint_to_article_model_dao(article))
                return article
            return CustomError("Error creating article", 400)
        except Exception:
            return CustomError("Internal Error", 500)

    def update_article_handler(self, id: int, article: ArticleModelDTOEndpoint) -> ArticleModelDTOEndpoint | CustomError:
        try:
            if (article.first_name is not None and
                    article.last_name is not None and
                    article.price is not None):
                self.service.update_article(id, convert_article_model_dto_endpoint_to_article_model_dao(article))
                return article
            return CustomError("Error updating article", 400)
        except Exception:
            return CustomError("Internal Error", 500)

    def delete_article_handler(self, id: int) -> None | CustomError:
        try:
            if self.service.exists_article_with_id(id):
                self.service.delete_article(id)
                return None
            return CustomError("Error deleting article", 404)
        except Exception:
            return CustomError("Internal Error", 500)
