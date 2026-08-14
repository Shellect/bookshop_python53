from pydantic import BaseModel

class BookResponse(BaseModel):
    title: str
    author: str
    poster: str
    price: int