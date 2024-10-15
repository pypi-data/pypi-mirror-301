from pydantic import BaseModel, ConfigDict, Field
from .category import Category
from .product import Product, ShortProduct


class ParentCategoriesResponse(BaseModel):
    categories: list[Category]


class CategoriesAndProductsBySlugParentCategory(BaseModel):
    date: str
    slug: str
    name: str
    url: str
    categories: list[Category]
    products: list[Product]


class NewProductsResponse(BaseModel):
    class Data(BaseModel):
        products: list[Product]

    class Meta(BaseModel):
        page: str
        totalPages: int
        totalCount: int
        pageSize: int

    data: Data
    _meta: Meta


class RemainsAndPlanresiduesResponse(BaseModel):
    date: str
    products: list[ShortProduct]


class TreeCategoriesResponse(BaseModel):
    tree: list[Category]
