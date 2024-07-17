from unittest.mock import patch, MagicMock
from app.database.db_connection import create_connection, close_connection


@patch("app.database.db_connection.psycopg2.connect")
def test_connection_successfully_established(mock_connect):
    mock_connect.return_value = MagicMock()
    connection = create_connection()

    assert connection is not None


@patch("app.database.db_connection.psycopg2.connect")
def test_connection_fails_with_exception(mock_connect):
    mock_connect.side_effect = Exception("Connection failed")
    connection = create_connection()

    assert connection is None


def test_connection_closed_successfully():
    mock_connection = MagicMock()
    close_connection(mock_connection)
    mock_connection.close.assert_called_once()


def test_close_connection_with_none_does_nothing():
    close_connection(None)
