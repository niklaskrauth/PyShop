import psycopg2

DATABASE_CONFIG = {
    "user": "python",
    "password": "python",
    "host": "localhost",
    "port": "5432",
    "database": "PyShop",
}


def create_connection():
    try:
        connection = psycopg2.connect(**DATABASE_CONFIG)
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Connection error", error)
        return None


def close_connection(connection):
    if connection:
        connection.close()
        print("Connection closed")
