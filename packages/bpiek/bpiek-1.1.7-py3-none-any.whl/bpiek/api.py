import requests

from bpiek.models.category import Category
from bpiek.models.product import Product
from bpiek.models.response import (
    CategoriesAndProductsBySlugParentCategory,
    NewProductsResponse,
    ParentCategoriesResponse,
    RemainsAndPlanresiduesResponse,
    TreeCategoriesResponse,
)

AUTH_URL = "https://bp.iek.ru/oauth/login"
API_URL = "https://bp.iek.ru/api/catalog/v1/"


class BPIekApi:
    def __init__(self) -> None:
        self.session = requests.Session()

    def _instance(self, endpoint: str, params: dict = {}):
        response = self.session.get(
            url=API_URL + endpoint,
            headers={"Content-Type": "application/json"},
            params={"format": "json", **params},
        )
        return response.json()

    def login(self, username: str, password: str) -> None:
        auth = self.session.post(
            url=f"{AUTH_URL}",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"username": username, "password": password},
        )

        if len(auth.cookies) == 0:
            raise Exception("Invalid username or password")

    def get_parent_categories(self) -> list[Category]:
        response = self._instance("client/catalog")

        try:
            result: ParentCategoriesResponse = ParentCategoriesResponse.model_validate(
                response
            )

            return result.categories

        except Exception as e:
            raise Exception(e)

    def get_product_by_article(self, article: str) -> Product:
        response = self._instance(f"client/products/{article}")

        try:
            result: Product = Product.model_validate(response)

            return result

        except Exception as e:
            raise Exception(e)

    def get_categories_and_products_by_slug_parent_category(
        self, slug: str
    ) -> CategoriesAndProductsBySlugParentCategory:
        response = self._instance(f"client/category/{slug}/json")

        try:
            result: CategoriesAndProductsBySlugParentCategory = (
                CategoriesAndProductsBySlugParentCategory.model_validate(response)
            )

            return result

        except Exception as e:
            raise Exception(e)

    def get_new_products(
        self,
        sortBy: str = "article",
        sortOrder: str = "asc",
        pageSize: int = 10,
        page: int = 1,
    ) -> NewProductsResponse:
        response = self._instance(
            "new-products",
            {sortBy: sortBy, sortOrder: sortOrder, pageSize: pageSize, page: page},
        )

        try:
            result: NewProductsResponse = NewProductsResponse.model_validate(response)

            return result

        except Exception as e:
            raise Exception(e)

    def get_remains_and_planresidues(self, slug: str) -> RemainsAndPlanresiduesResponse:
        response = self._instance(f"client/category/{slug}/balances-json")

        try:
            result: RemainsAndPlanresiduesResponse = (
                RemainsAndPlanresiduesResponse.model_validate(response)
            )

            return result

        except Exception as e:
            raise Exception(e)

    def get_tree_categories(self, parent_code: str = "00") -> list[Category]:
        tree = {}

        def convert_to_nested_list(nested_dict: dict, parent_code: str = "00") -> list:
            result = []
            for idx, (key, value) in enumerate(nested_dict.items()):
                if isinstance(value, dict):
                    try:
                        code = (
                            f"{parent_code}.{str(idx).zfill(2)}"
                            if parent_code
                            else f"{str(idx).zfill(2)}"
                        )
                        result.append(
                            {
                                "name": value["name"],
                                "slug": value["slug"],
                                "url": value["url"],
                                "code": code,
                                "childs": convert_to_nested_list(value["childs"], code),
                            }
                        )
                    except:
                        continue
                else:
                    result.append(value)
            return result

        def convert_list_to_nested_dict(_list: list):
            def update_nested(d, keys, value):
                for key in keys[:-1]:
                    d = d.setdefault(key, {})
                d[keys[-1]] = value

            tmp_categories = _list.copy()

            for idx, category in enumerate(tmp_categories):
                paths = category.url[1:][:-1].split("/")

                _str = ""
                for _idx, path in enumerate(paths):
                    if len(paths) == _idx + 1:
                        _str += f"{path}"
                        break

                    _str += f"{path},childs,"

                try:
                    update_nested(
                        tree,
                        _str.split(","),
                        {
                            "name": category.name,
                            "slug": category.slug,
                            "url": category.url,
                            "childs": {},
                        },
                    )

                    tmp_categories.pop(idx)
                except Exception as e:
                    print(e)
                    continue

            return tmp_categories

        for parent_category in self.get_parent_categories():
            tree[parent_category.slug] = {
                "name": parent_category.name,
                "slug": parent_category.slug,
                "url": parent_category.url,
                "childs": {},
            }
            categories_and_products = (
                self.get_categories_and_products_by_slug_parent_category(
                    slug=parent_category.slug
                )
            )
            tmp_categories = convert_list_to_nested_dict(
                categories_and_products.categories
            )
            while len(tmp_categories) != 0:
                tmp_categories = convert_list_to_nested_dict(tmp_categories)

        return TreeCategoriesResponse.model_validate(
            {"tree": convert_to_nested_list(tree, parent_code)}
        ).tree
