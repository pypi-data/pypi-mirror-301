from enum import Enum
from typing import Literal


class ArticleAccessRight(str, Enum):
    CLOSED = "Closed"
    NA = "na"
    OPENPRIVATE = "OpenPrivate"
    OPENPUBLIC = "OpenPublic"

    def __str__(self) -> str:
        return str(self.value)


ArticleAccessRightLiteral = Literal[
    "Closed",
    "na",
    "OpenPrivate",
    "OpenPublic",
]
