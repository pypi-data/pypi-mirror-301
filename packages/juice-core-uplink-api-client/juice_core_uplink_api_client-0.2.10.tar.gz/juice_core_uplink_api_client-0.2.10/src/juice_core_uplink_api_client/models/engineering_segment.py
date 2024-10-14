from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EngineeringSegment")


@_attrs_define
class EngineeringSegment:
    """
    Attributes:
        start (str):
        end (str):
        segment_type (Union[Unset, str]):
        power (Union[Unset, float]):
        segment_type_raw (Union[Unset, str]):
    """

    start: str
    end: str
    segment_type: Unset | str = UNSET
    power: Unset | float = UNSET
    segment_type_raw: Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start = self.start

        end = self.end

        segment_type = self.segment_type

        power = self.power

        segment_type_raw = self.segment_type_raw

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start": start,
                "end": end,
            }
        )
        if segment_type is not UNSET:
            field_dict["segment_type"] = segment_type
        if power is not UNSET:
            field_dict["power"] = power
        if segment_type_raw is not UNSET:
            field_dict["segment_type_raw"] = segment_type_raw

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        start = d.pop("start")

        end = d.pop("end")

        segment_type = d.pop("segment_type", UNSET)

        power = d.pop("power", UNSET)

        segment_type_raw = d.pop("segment_type_raw", UNSET)

        engineering_segment = cls(
            start=start,
            end=end,
            segment_type=segment_type,
            power=power,
            segment_type_raw=segment_type_raw,
        )

        engineering_segment.additional_properties = d
        return engineering_segment

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
