from loguru import logger

from app.models.dao.article_model_dao import ArticlesModelDAO, ArticleModelDAO
from app.models.dto.article_model_dto import (
    ArticlesModelDTO,
    ArticleModelDTO,
    ArticleModelDTOEndpoint,
)


def convert_articles_model_dao_to_articles_model_dto(
    articles_dao: ArticlesModelDAO,
) -> ArticlesModelDTO | Exception:
    try:
        articles_dto = ArticlesModelDTO(articles=[])

        print(articles_dao)
        for article_dao in articles_dao:
            article_dto = ArticleModelDTO(
                id=article_dao[0],
                imageUrl=article_dao[1],
                first_name=article_dao[2],
                last_name=article_dao[3],
                price=article_dao[4],
            )
            articles_dto.articles.append(article_dto)
        return articles_dto
    except Exception as e:
        logger.error(f"Error converting articles model dao to articles model dto: {e}")
        return e


def convert_list_to_article_model_dto(article: list) -> ArticleModelDTO | Exception:
    try:
        article_dict = dict(
            zip(["id", "imageUrl", "first_name", "last_name", "price"], article)
        )
        article_dto = ArticleModelDTO(**article_dict)
        return article_dto
    except Exception as e:
        logger.error(f"Error converting list to article model dto: {e}")
        return e


def convert_article_model_dto_endpoint_to_article_model_dao(
    article_dto_endpoint: ArticleModelDTOEndpoint,
) -> ArticleModelDAO | Exception:
    try:
        article_dao = ArticleModelDAO(
            id=0,
            imageUrl=article_dto_endpoint.imageUrl,
            first_name=article_dto_endpoint.first_name,
            last_name=article_dto_endpoint.last_name,
            price=article_dto_endpoint.price,
        )
        return article_dao
    except Exception as e:
        logger.error(
            f"Error converting article model dto endpoint to article model dao: {e}"
        )
        return e
