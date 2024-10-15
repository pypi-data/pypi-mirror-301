from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic.types import UUID1


class Category(BaseModel):
    code: str | None = Field(default=None)  # Код категории
    slug: str  # Слаг категории
    name: str  # Название категории
    url: str  # Относительный адрес категории
    apiUrl: str | None = Field(
        default=None
    )  # Ссылка на скачивание файла с содержимым категории
    childs: list["Category"] | None = Field(default=[])
