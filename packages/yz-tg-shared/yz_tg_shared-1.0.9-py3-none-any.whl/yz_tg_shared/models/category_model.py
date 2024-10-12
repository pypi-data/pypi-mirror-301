from pydantic import BaseModel


class CategoryModel(BaseModel):
    CategoryID: int
    CategoryName: str
    Description: str

    class Config:
        orm_mode = True
