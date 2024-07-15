from typing import Optional

from pydantic import BaseModel


class ArticleModelDTO(BaseModel):
    id: int
    imageUrl: Optional[str] = ""
    first_name: str
    last_name: str
    price: float


class ArticleModelDTOEndpoint(BaseModel):
    imageUrl: Optional[str] = ""
    first_name: str
    last_name: str
    price: float

class ArticlesModelDTO(BaseModel):
    articles: list[ArticleModelDTO]

