import pytest
from starlette.testclient import TestClient

from app.handlers.article_handler import ArticleHandler
from app.main import app
from app.models.dto.article_model_dto import (
    ArticlesModelDTO,
    ArticleModelDTO,
    ArticleModelDTOEndpoint,
)

client = TestClient(app)


@pytest.fixture
def article_handler(article_service_mock):
    return ArticleHandler(article_service_mock)


@pytest.fixture
def article_service_mock(mocker):
    return mocker.Mock()


##################################################################### Tests for get_articles_handler ########################################################################


def test_get_articles_handler_returns_success_when_articles_exist(
    article_handler, mocker
):
    articles_dao = [(1, "http://example.com/image.jpg", "John", "Doe", 100)]
    articles_dto = ArticlesModelDTO(
        articles=[
            ArticleModelDTO(
                id=1,
                imageUrl="http://example.com/image.jpg",
                first_name="John",
                last_name="Doe",
                price=100.0,
            )
        ]
    )

    mocker.patch.object(
        article_handler.service, "get_all_articles", return_value=articles_dao
    )
    mocker.patch(
        "app.util.converter.convert_articles_model_dao_to_articles_model_dto",
        return_value=articles_dto,
    )

    response = article_handler.get_articles_handler()

    assert response.status_code == 200
    assert response.body.decode() == (
        '{"articles":[{"id":1,"imageUrl":"http://example.com/image.jpg",'
        '"first_name":"John","last_name":"Doe","price":100.0}]}'
    )


def test_get_articles_handler_returns_not_found_when_no_articles_exist(
    article_handler, mocker
):
    mocker.patch.object(
        article_handler.service,
        "get_all_articles",
        return_value=None,
    )

    response = article_handler.get_articles_handler()

    assert response.status_code == 404
    assert response.body.decode() == '{"message":"No articles found"}'


def test_get_articles_handler_returns_internal_server_error_on_exception(
    article_handler, mocker
):
    mocker.patch.object(
        article_handler.service,
        "get_all_articles",
        side_effect=Exception("Database error"),
    )

    response = article_handler.get_articles_handler()

    assert response.status_code == 500
    assert response.body.decode() == '{"message":"Internal Server Error"}'


##################################################################### Tests for get_articles_handler ########################################################################


def test_get_article_handler_returns_success_when_article_exist(
    article_handler, mocker
):
    article_list = (1, "http://example.com/image.jpg", "John", "Doe", 100)
    article_dto = ArticleModelDTO(
        id=1,
        imageUrl="http://example.com/image.jpg",
        first_name="John",
        last_name="Doe",
        price=100.0,
    )

    mocker.patch.object(
        article_handler.service, "get_article", return_value=article_list
    )
    mocker.patch(
        "app.util.converter.convert_list_to_article_model_dto",
        return_value=article_dto,
    )

    response = article_handler.get_article_handler(1)

    assert response.status_code == 200
    assert response.body.decode() == (
        '{"id":1,"imageUrl":"http://example.com/image.jpg",'
        '"first_name":"John","last_name":"Doe","price":100.0}'
    )


def test_get_article_handler_returns_not_found_when_no_article_exist(
    article_handler, mocker
):
    mocker.patch.object(
        article_handler.service,
        "get_article",
        return_value=None,
    )

    response = article_handler.get_article_handler(100)

    assert response.status_code == 404
    assert response.body.decode() == '{"message":"Article not found"}'


def test_get_article_handler_returns_internal_server_error_on_exception(
    article_handler, mocker
):
    mocker.patch.object(
        article_handler.service,
        "get_article",
        side_effect=Exception("Database error"),
    )

    response = article_handler.get_article_handler(1)

    assert response.status_code == 500
    assert response.body.decode() == '{"message":"Internal Server Error"}'


##################################################################### Tests for create_article_handler ########################################################################


def test_create_article_handler_success(article_handler, mocker):
    article = ArticleModelDTOEndpoint(first_name="John", last_name="Doe", price=100)

    mocker.patch.object(
        article_handler.service,
        "create_article",
        return_value=None,
    )

    response = article_handler.create_article_handler(article)

    assert response.status_code == 200
    assert (
        response.body.decode()
        == '{"imageUrl":"","first_name":"John","last_name":"Doe","price":100.0}'
    )


def test_create_article_handler_exception(article_handler, mocker):
    article = ArticleModelDTOEndpoint(first_name="John", last_name="Doe", price=100)

    mocker.patch.object(
        article_handler.service,
        "create_article",
        side_effect=Exception("Database error"),
    )

    response = article_handler.create_article_handler(article)

    assert response.status_code == 500
    assert response.body.decode() == '{"message":"Internal Server Error"}'


##################################################################### Tests for update_article_handler ########################################################################


def test_update_article_handler_returns_success_when_updated(article_handler, mocker):
    article = ArticleModelDTOEndpoint(first_name="Jane", last_name="Doe", price=100)

    mocker.patch.object(
        article_handler.service,
        "update_article",
        return_value=None,
    )

    response = article_handler.update_article_handler(1, article)

    assert response.status_code == 200
    assert response.body.decode() == (
        '{"imageUrl":"",' '"first_name":"Jane","last_name":"Doe","price":100.0}'
    )


def test_update_article_handler_returns_internal_server_error_on_exception(
    article_handler, mocker
):
    article = ArticleModelDTOEndpoint(first_name="Jane", last_name="Doe", price=100)

    mocker.patch.object(
        article_handler.service,
        "update_article",
        side_effect=Exception("Database error"),
    )

    response = article_handler.update_article_handler(1, article)

    assert response.status_code == 500
    assert response.body.decode() == '{"message":"Internal Server Error"}'


##################################################################### Tests for delete_article_handler ########################################################################


def test_delete_article_handler_returns_success_when_deleted(article_handler, mocker):
    mocker.patch.object(
        article_handler.service,
        "delete_article",
        return_value=None,
    )

    response = article_handler.delete_article_handler(1)

    assert response.status_code == 200
    assert response.body.decode() == '{"message":"Article deleted successfully!"}'


def test_delete_article_handler_returns_not_found_when_id_is_invalid(
    article_handler, mocker
):
    mocker.patch.object(
        article_handler.service,
        "delete_article",
        return_value=None,
    )

    mocker.patch.object(
        article_handler.service,
        "exists_article_with_id",
        return_value=False,
    )

    response = article_handler.delete_article_handler(999)

    assert response.status_code == 404
    assert response.body.decode() == '{"message":"Article not found"}'


def test_delete_article_handler_returns_internal_server_error_on_exception(
    article_handler, mocker
):
    mocker.patch.object(
        article_handler.service,
        "delete_article",
        side_effect=Exception("Database error"),
    )

    response = article_handler.delete_article_handler(1)

    assert response.status_code == 500
    assert response.body.decode() == '{"message":"Internal Server Error"}'
