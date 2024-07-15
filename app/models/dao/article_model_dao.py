from typing import Optional

from pydantic import BaseModel


class ArticleModelDAO(BaseModel):
    id: int
    imageUrl: Optional[str] = ""
    first_name: str
    last_name: str
    price: float


class ArticlesModelDAO(BaseModel):
    articles: list[ArticleModelDAO]


