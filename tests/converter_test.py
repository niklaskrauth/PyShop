import unittest

import pytest

from app.models.dao.article_model_dao import ArticlesModelDAO, ArticleModelDAO
from app.models.dto.article_model_dto import (
    ArticleModelDTOEndpoint,
    ArticlesModelDTO,
    ArticleModelDTO,
)
from app.util.converter import (
    convert_articles_model_dao_to_articles_model_dto,
    convert_list_to_article_model_dto,
    convert_article_model_dto_endpoint_to_article_model_dao,
)


class TestConverter(unittest.TestCase):
    pass


@pytest.fixture
def article_list():
    return [3, "http://example.com/image3.jpg", "Jake", "Doe", 200]


@pytest.fixture
def article_model_dto_endpoint():
    return ArticleModelDTOEndpoint(
        imageUrl="http://example.com/image4.jpg",
        first_name="Jill",
        last_name="Doe",
        price=250,
    )


def test_conversion_from_dao_to_dto_succeeds():
    articles_dao = [
        (1, "http://example.com/image1.jpg", "John", "Doe", 100),
        (2, "http://example.com/image2.jpg", "Jane", "Doe", 150),
    ]

    result = convert_articles_model_dao_to_articles_model_dto(articles_dao)

    assert isinstance(result, ArticlesModelDTO)
    assert len(result.articles) == 2

    assert result.articles[0].first_name == "John"
    assert result.articles[0].last_name == "Doe"
    assert result.articles[0].imageUrl == "http://example.com/image1.jpg"
    assert result.articles[0].price == 100

    assert result.articles[1].first_name == "Jane"
    assert result.articles[1].last_name == "Doe"
    assert result.articles[1].imageUrl == "http://example.com/image2.jpg"
    assert result.articles[1].price == 150


def test_conversion_from_dao_to_dto_fails_on_bad_data():
    bad_data = [("", None, " ", " ", " "), ("", None, " ", " ", " ")]

    result = convert_articles_model_dao_to_articles_model_dto(bad_data)

    assert isinstance(result, Exception)


def test_conversion_from_list_to_dto_succeeds(article_list):
    result = convert_list_to_article_model_dto(article_list)

    assert isinstance(result, ArticleModelDTO)
    assert result.first_name == "Jake"
    assert result.last_name == "Doe"
    assert result.imageUrl == "http://example.com/image3.jpg"
    assert result.price == 200


def test_conversion_from_list_to_dto_fails_on_bad_data():
    bad_data = ["only_one_field"]
    result = convert_list_to_article_model_dto(bad_data)

    assert isinstance(result, Exception)


def test_conversion_from_dto_endpoint_to_dao_succeeds(article_model_dto_endpoint):
    result = convert_article_model_dto_endpoint_to_article_model_dao(
        article_model_dto_endpoint
    )

    assert isinstance(result, ArticleModelDAO)
    assert result.first_name == "Jill"
    assert result.last_name == "Doe"
    assert result.imageUrl == "http://example.com/image4.jpg"
    assert result.price == 250
