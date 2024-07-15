from pydantic import BaseModel


class CustomErrorModel(BaseModel):
    message: str
    status_code: int
