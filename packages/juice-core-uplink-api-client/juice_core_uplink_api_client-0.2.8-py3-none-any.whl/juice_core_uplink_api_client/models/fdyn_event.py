from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FdynEvent")


@_attrs_define
class FdynEvent:
    """
    Attributes:
        name (str):
        count (int):
        start (Union[None, Unset, str]):
        end (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        definition (Union[Unset, str]):
    """

    name: str
    count: int
    start: None | Unset | str = UNSET
    end: None | Unset | str = UNSET
    description: None | Unset | str = UNSET
    definition: Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        count = self.count

        start: None | Unset | str
        if isinstance(self.start, Unset):
            start = UNSET
        else:
            start = self.start

        end: None | Unset | str
        if isinstance(self.end, Unset):
            end = UNSET
        else:
            end = self.end

        description: None | Unset | str
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        definition = self.definition

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "count": count,
            }
        )
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end
        if description is not UNSET:
            field_dict["description"] = description
        if definition is not UNSET:
            field_dict["definition"] = definition

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        count = d.pop("count")

        def _parse_start(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        start = _parse_start(d.pop("start", UNSET))

        def _parse_end(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        end = _parse_end(d.pop("end", UNSET))

        def _parse_description(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        description = _parse_description(d.pop("description", UNSET))

        definition = d.pop("definition", UNSET)

        fdyn_event = cls(
            name=name,
            count=count,
            start=start,
            end=end,
            description=description,
            definition=definition,
        )

        fdyn_event.additional_properties = d
        return fdyn_event

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
