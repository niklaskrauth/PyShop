import pytest
from starlette.responses import JSONResponse

from app.handlers.article_handler import ArticleHandler


@pytest.fixture
def mock_article_handler(mocker):
    handler = mocker.Mock(spec=ArticleHandler)
    return handler


def test_fetching_articles_successfully_returns_article_list(mock_article_handler):
    mock_article_handler.get_articles_handler.return_value = JSONResponse(
        status_code=200,
        content=[{"id": 1, "title": "Test Article", "content": "Test Content"}]
    )
    response = mock_article_handler.get_articles_handler()
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["title"] == "Test Article"


def test_fetching_articles_when_none_exist_returns_404(mock_article_handler):
    mock_article_handler.get_articles_handler.return_value = JSONResponse(
        status_code=404,
        content={"message": "Articles not found"}
    )
    response = mock_article_handler.get_articles_handler()
    assert response.status_code == 404
    assert response.json()["message"] == "Articles not found"


def test_fetching_articles_raises_internal_server_error_on_exception(mock_article_handler):
    mock_article_handler.get_articles_handler.side_effect = Exception("Database error")
    response = mock_article_handler.get_articles_handler()
    assert response.status_code == 500
    assert response.json()["message"] == "Internal Server Error"
