from enum import Enum
from typing import Literal


class FindArticlesResolve(str, Enum):
    COLLECTION = "collection"
    TAGS = "tags"

    def __str__(self) -> str:
        return str(self.value)


FindArticlesResolveLiteral = Literal[
    "collection",
    "tags",
]
