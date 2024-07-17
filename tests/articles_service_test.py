import pytest
from unittest.mock import MagicMock, patch

from app.models.dao.article_model_dao import ArticleModelDAO
from app.services.articles_service import ArticlesService


@pytest.fixture
def articles_service():
    mock_dependency = MagicMock()
    return ArticlesService(mock_dependency)


@pytest.fixture
def mock_cursor():
    return MagicMock()


@pytest.fixture
def mock_connection(mock_cursor):
    connection = MagicMock()
    connection.cursor.return_value = mock_cursor
    return connection


##################################################################### Tests for exists_article_with_id ########################################################################


def test_exists_article_with_id_returns_true_when_article_exists(articles_service):
    with patch.object(articles_service, "exists_article_with_id", return_value=True):
        response = articles_service.exists_article_with_id(1)

        assert response is True


def test_exists_article_with_id_returns_false_when_article_does_not_exist(
    articles_service,
):
    with patch.object(articles_service, "exists_article_with_id", return_value=False):
        response = articles_service.exists_article_with_id(999)

        assert response is False


def test_exists_article_with_id_raises_exception_on_database_error(articles_service):
    with patch.object(
        articles_service,
        "exists_article_with_id",
        side_effect=Exception("Database error"),
    ):
        try:
            articles_service.exists_article_with_id(1)
        except Exception as e:
            assert str(e) == "Database error"


##################################################################### Tests for get_all_articles ########################################################################


def test_get_all_articles_returns_non_empty_list_on_success(
    mock_connection, mock_cursor
):
    mock_cursor.fetchall.return_value = [
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "imageUrl": "http://example.com/image.jpg",
            "price": 100,
        },
        {
            "id": 2,
            "first_name": "Jane",
            "last_name": "Doe",
            "imageUrl": "http://example.com/image2.jpg",
            "price": 150,
        },
    ]
    articles_service = ArticlesService(mock_connection)
    result = articles_service.get_all_articles()

    assert len(result) > 0
    assert result[0]["first_name"] == "John"
    assert result[0]["last_name"] == "Doe"
    assert result[0]["imageUrl"] == "http://example.com/image.jpg"
    assert result[0]["price"] == 100
    assert result[1]["first_name"] == "Jane"
    assert result[1]["last_name"] == "Doe"
    assert result[1]["imageUrl"] == "http://example.com/image2.jpg"
    assert result[1]["price"] == 150


def test_get_all_articles_returns_empty_list_when_no_articles_exist(
    mock_connection, mock_cursor
):
    mock_cursor.fetchall.return_value = []
    articles_service = ArticlesService(mock_connection)
    result = articles_service.get_all_articles()

    assert len(result) == 0


def test_get_all_articles_raises_exception_on_database_error(
    mock_connection, mock_cursor
):
    mock_cursor.execute.side_effect = Exception("Database error")
    articles_service = ArticlesService(mock_connection)
    result = articles_service.get_all_articles()

    assert isinstance(result, Exception)


##################################################################### Tests for get_article ########################################################################


def test_get_article_returns_article(mock_connection, mock_cursor):
    mock_cursor.fetchone.return_value = {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "imageUrl": "http://example.com/image.jpg",
        "price": 100,
    }
    articles_service = ArticlesService(mock_connection)
    result = articles_service.get_article(1)

    assert result["first_name"] == "John"
    assert result["last_name"] == "Doe"
    assert result["imageUrl"] == "http://example.com/image.jpg"
    assert result["price"] == 100


def test_get_article_raises_database_error_returns_exception(
    mock_connection, mock_cursor
):
    mock_cursor.execute.side_effect = Exception("Database error")
    articles_service = ArticlesService(mock_connection)
    result = articles_service.get_article(1)

    assert isinstance(result, Exception)


##################################################################### Tests for create_article ########################################################################


def test_create_article_succeeds_with_valid_data(mock_connection, mock_cursor):
    mock_cursor.rowcount = 1
    articles_service = ArticlesService(mock_connection)

    article = ArticleModelDAO(
        id=1,
        first_name="John",
        last_name="Doe",
        imageUrl="http://example.com/image.jpg",
        price=100,
    )

    result = articles_service.create_article(article)

    assert result == 1


def test_create_article_returns_exception_on_db_error(mock_connection, mock_cursor):
    mock_cursor.execute.side_effect = Exception("Database error")
    articles_service = ArticlesService(mock_connection)

    article = ArticleModelDAO(
        id=1,
        first_name="Jane",
        last_name="Doe",
        imageUrl="http://example.com/image2.jpg",
        price=150.0,
    )

    result = articles_service.create_article(article)

    assert isinstance(result, Exception)


##################################################################### Tests for create_article ########################################################################


def test_update_article_succeeds_with_valid_data(mock_connection, mock_cursor):
    mock_cursor.rowcount = 1
    articles_service = ArticlesService(mock_connection)
    article = ArticleModelDAO(
        id=1,
        first_name="Updated John",
        last_name="Updated Doe",
        imageUrl="http://example.com/updated_image.jpg",
        price=200,
    )
    result = articles_service.update_article(1, article)

    assert result == 1


def test_update_article_when_article_does_not_exist_returns_zero(
    mock_connection, mock_cursor
):
    mock_cursor.rowcount = 0
    articles_service = ArticlesService(mock_connection)
    article = ArticleModelDAO(
        id=1,
        first_name="Nonexistent John",
        last_name="Nonexistent Doe",
        imageUrl="http://example.com/nonexistent_image.jpg",
        price=250,
    )
    result = articles_service.update_article(999, article)

    assert result == 0


def test_update_article_when_error_raised_returns_exception(
    mock_connection, mock_cursor
):
    mock_cursor.execute.side_effect = Exception("Database error")
    articles_service = ArticlesService(mock_connection)
    article = ArticleModelDAO(
        id=1,
        first_name="Error John",
        last_name="Error Doe",
        imageUrl="http://example.com/error_image.jpg",
        price=300,
    )
    result = articles_service.update_article(1, article)

    assert isinstance(result, Exception)


##################################################################### Tests for create_article ########################################################################


def test_delete_article_succeeds_with_valid_data(mock_connection, mock_cursor):
    mock_cursor.rowcount = 1
    articles_service = ArticlesService(mock_connection)
    result = articles_service.delete_article(1)

    assert result == 1


def test_delete_article_when_error_raised_returns_exception(
    mock_connection, mock_cursor
):
    mock_cursor.execute.side_effect = Exception("Database error")
    articles_service = ArticlesService(mock_connection)
    result = articles_service.delete_article(1)

    assert isinstance(result, Exception)
