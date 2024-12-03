from pydantic import BaseModel


class Product(BaseModel):
    code: str
    label: str
    image: str
    quantity: int
    category: str
    seller: str
    sender: str

    class Config:
        from_attributes = True
