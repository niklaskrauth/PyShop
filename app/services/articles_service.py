from app.models.dao.article_model_dao import ArticlesModelDAO, ArticleModelDAO


class ArticlesService:
    def __init__(self, connection):
        self.connection = connection

    def exists_article_with_id(self, id: int) -> bool:
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM articles WHERE id = %s", (id,))
                if cursor.fetchone():
                    return True
                return False
            except Exception:
                return False

    def get_all_articles(self) -> ArticlesModelDAO | Exception:
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM articles")
                return cursor.fetchall()
            except Exception as e:
                return e

    def get_article(self, id: int) -> list | Exception:
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM articles WHERE id = %s", (id,))
                return cursor.fetchone()
            except Exception as e:
                return e

    def create_article(self, article: ArticleModelDAO) -> None | Exception:
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute(
                    "INSERT INTO articles (first_name, last_name, imageUrl, price) VALUES (%s, %s, %s, %s)",
                    (
                        article.first_name,
                        article.last_name,
                        article.imageUrl,
                        article.price,
                    ),
                )
                cursor.connection.commit()
                return cursor.rowcount
            except Exception as e:
                return e

    def update_article(self, id: int, article: ArticleModelDAO) -> None | Exception:
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute(
                    "UPDATE articles SET first_name = %s, last_name = %s, imageUrl = %s, price = %s WHERE id = %s",
                    (
                        article.first_name,
                        article.last_name,
                        article.imageUrl,
                        article.price,
                        id,
                    ),
                )
                cursor.connection.commit()
                return cursor.rowcount
            except Exception as e:
                return e

    def delete_article(self, id: int) -> None | Exception:
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute("DELETE FROM articles WHERE id = %s", (id,))
                cursor.connection.commit()
                return cursor.rowcount
            except Exception as e:
                return e
