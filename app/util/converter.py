from app.errors.custom_error import CustomError
from app.models.dao.article_model_dao import ArticlesModelDAO, ArticleModelDAO
from app.models.dto.article_model_dto import ArticlesModelDTO, ArticleModelDTO, ArticleModelDTOEndpoint


def convert_articles_model_dao_to_articles_model_dto(articles_dao: ArticlesModelDAO) -> ArticlesModelDTO | Exception:
    try:
        articles_dto = ArticlesModelDTO(articles=[])
        for article_dao in articles_dao:
            article_dto = ArticleModelDTO(
                id=article_dao[0],
                imageUrl=article_dao[1],
                first_name=article_dao[2],
                last_name=article_dao[3],
                price=article_dao[4]
            )
            articles_dto.articles.append(article_dto)
        return articles_dto
    except Exception:
        return CustomError("Error converting articles model dao to articles model dto", 500)


def convert_list_to_article_model_dto(article: list) -> ArticleModelDTO | Exception:
    try:
        article_dict = dict(zip(["id", "imageUrl", "first_name", "last_name", "price"], article))
        article_dto = ArticleModelDTO(**article_dict)
        return article_dto
    except Exception:
        return CustomError("Error converting list to article model dto", 500)


def convert_article_model_dto_endpoint_to_article_model_dao(article_dto_endpoint: ArticleModelDTOEndpoint) -> (
        ArticleModelDAO | Exception):
    try:
        article_dao = ArticleModelDAO(
            id=0,
            imageUrl=article_dto_endpoint.imageUrl,
            first_name=article_dto_endpoint.first_name,
            last_name=article_dto_endpoint.last_name,
            price=article_dto_endpoint.price
        )
        return article_dao
    except Exception:
        return CustomError("Error converting article model dto to article model dao", 500)
