from pydantic import BaseModel


class Request(BaseModel):
    base64: str
