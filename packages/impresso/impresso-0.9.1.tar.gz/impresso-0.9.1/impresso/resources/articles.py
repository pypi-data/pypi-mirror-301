from typing import Any, Union

from pandas import DataFrame, json_normalize

from impresso.api_client.api.articles import find_articles, get_article
from impresso.api_client.models.find_articles_order_by import (
    FindArticlesOrderBy,
    FindArticlesOrderByLiteral,
)
from impresso.api_client.models.find_articles_resolve import (
    FindArticlesResolve,
    FindArticlesResolveLiteral,
)
from impresso.api_client.types import UNSET, Unset
from impresso.api_models import Article, BaseFind
from impresso.data_container import DataContainer
from impresso.resources.base import Resource
from impresso.util.error import raise_for_error
from impresso.util.py import get_enum_from_literal


class ArticlesResponseSchema(BaseFind):
    """Schema for the articles response."""

    data: list[Article]


class ArticlesDataContainer(DataContainer):
    """Response of an articles call."""

    @property
    def df(self) -> DataFrame:
        """Return the data as a pandas dataframe."""
        return json_normalize(self._data.to_dict()["data"]).set_index("uid")


class ArticleDataContainer(DataContainer):
    """Response of a get article call."""

    @property
    def raw(self) -> dict[str, Any]:
        """Return the data as a python dictionary."""
        return self._data.to_dict()

    @property
    def pydantic(self) -> Article:
        """Return the data as a pydantic model."""
        return self._pydantic_model.model_validate(self.raw)

    @property
    def df(self) -> DataFrame:
        """Return the data as a pandas dataframe."""
        return json_normalize([self.raw])

    @property
    def size(self) -> int:
        """Current page size."""
        data = self._data.to_dict()
        if len(data):
            return 1
        return 0

    @property
    def total(self) -> int:
        """Total number of results."""
        return self.size


class ArticlesResource(Resource):
    """Get articles from the impresso database."""

    name = "articles"

    def find(
        self,
        resolve: Union[Unset, FindArticlesResolveLiteral] = UNSET,
        order_by: Union[Unset, FindArticlesOrderByLiteral] = UNSET,
        limit: Union[Unset, int] = UNSET,
        offset: Union[Unset, int] = UNSET,
    ):
        result = find_articles.sync(
            client=self._api_client,
            resolve=get_enum_from_literal(resolve, FindArticlesResolve),
            order_by=get_enum_from_literal(order_by, FindArticlesOrderBy),
            limit=limit,
            offset=offset,
        )
        raise_for_error(result)
        return ArticlesDataContainer(result, ArticlesResponseSchema)

    def get(self, id: str):
        result = get_article.sync(client=self._api_client, id=id)
        raise_for_error(result)

        id_parts = id.split("-")
        issue_id = "-".join(id_parts[:-1])
        article_id = id_parts[-1]

        return ArticleDataContainer(
            result,
            Article,
            f"{self._get_web_app_base_url()}/issue/{issue_id}/view?articleId={article_id}",
        )
