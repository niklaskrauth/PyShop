import pytest
from pytest_mock import mocker

from app.services.articles_service import ArticlesService


@pytest.fixture
def mock_cursor(mocker):
    return mocker.MagicMock()


@pytest.fixture
def test_mock_connection(mock_cursor):
    connection = mocker.MagicMock()
    connection.cursor.return_value = mock_cursor
    return connection


def test_article_exists_with_valid_id_returns_true(mock_connection, mock_cursor):
    mock_cursor.fetchone.return_value = True
    articles_service = ArticlesService(mock_connection)
    assert articles_service.exists_article_with_id(1) is True


def test_article_does_not_exist_with_invalid_id_returns_false(
    mock_connection, mock_cursor
):
    mock_cursor.fetchone.return_value = None
    articles_service = ArticlesService(mock_connection)
    assert articles_service.exists_article_with_id(999) is False


def test_article_exists_raises_exception_on_database_error(
    mock_connection, mock_cursor
):
    mock_cursor.execute.side_effect = Exception("Database error")
    articles_service = ArticlesService(mock_connection)
    assert articles_service.exists_article_with_id(1) is False
