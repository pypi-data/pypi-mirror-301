from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UvtEvent")


@_attrs_define
class UvtEvent:
    """
    Attributes:
        count (int):
        mnemonic (str):
        time (Union[None, Unset, str]):
        name (Union[Unset, str]):
        source (Union[Unset, str]):
        duration (Union[None, Unset, str]):
    """

    count: int
    mnemonic: str
    time: None | Unset | str = UNSET
    name: Unset | str = UNSET
    source: Unset | str = UNSET
    duration: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        mnemonic = self.mnemonic

        time: None | Unset | str
        if isinstance(self.time, Unset):
            time = UNSET
        else:
            time = self.time

        name = self.name

        source = self.source

        duration: None | Unset | str
        if isinstance(self.duration, Unset):
            duration = UNSET
        else:
            duration = self.duration

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
                "mnemonic": mnemonic,
            }
        )
        if time is not UNSET:
            field_dict["time"] = time
        if name is not UNSET:
            field_dict["name"] = name
        if source is not UNSET:
            field_dict["source"] = source
        if duration is not UNSET:
            field_dict["duration"] = duration

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        count = d.pop("count")

        mnemonic = d.pop("mnemonic")

        def _parse_time(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        time = _parse_time(d.pop("time", UNSET))

        name = d.pop("name", UNSET)

        source = d.pop("source", UNSET)

        def _parse_duration(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        duration = _parse_duration(d.pop("duration", UNSET))

        uvt_event = cls(
            count=count,
            mnemonic=mnemonic,
            time=time,
            name=name,
            source=source,
            duration=duration,
        )

        uvt_event.additional_properties = d
        return uvt_event

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
