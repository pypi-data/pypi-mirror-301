from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="TopicRelatedTopicsItem")


@_attrs_define
class TopicRelatedTopicsItem:
    """
    Attributes:
        uid (str): The unique identifier of the related topic
        w (float): TODO
    """

    uid: str
    w: float

    def to_dict(self) -> Dict[str, Any]:
        uid = self.uid

        w = self.w

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "uid": uid,
                "w": w,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        uid = d.pop("uid")

        w = d.pop("w")

        topic_related_topics_item = cls(
            uid=uid,
            w=w,
        )

        return topic_related_topics_item
