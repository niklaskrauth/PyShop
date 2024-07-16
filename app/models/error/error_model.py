from pydantic import BaseModel


class ErrorResponseModel(BaseModel):
    message: str
