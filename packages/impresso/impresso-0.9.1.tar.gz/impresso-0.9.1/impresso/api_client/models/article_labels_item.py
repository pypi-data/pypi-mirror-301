from enum import Enum
from typing import Literal


class ArticleLabelsItem(str, Enum):
    ARTICLE = "article"

    def __str__(self) -> str:
        return str(self.value)


ArticleLabelsItemLiteral = Literal["article",]
