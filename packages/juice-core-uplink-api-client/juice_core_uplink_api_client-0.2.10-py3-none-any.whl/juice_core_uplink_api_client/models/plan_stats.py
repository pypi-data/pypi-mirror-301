from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PlanStats")


@_attrs_define
class PlanStats:
    """
    Attributes:
        segment_number (Union[Unset, str]):
        group_number (Union[Unset, str]):
        start (Union[Unset, str]):
        end (Union[Unset, str]):
        stats (Union[Unset, str]):
    """

    segment_number: Unset | str = UNSET
    group_number: Unset | str = UNSET
    start: Unset | str = UNSET
    end: Unset | str = UNSET
    stats: Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        segment_number = self.segment_number

        group_number = self.group_number

        start = self.start

        end = self.end

        stats = self.stats

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if segment_number is not UNSET:
            field_dict["segment_number"] = segment_number
        if group_number is not UNSET:
            field_dict["group_number"] = group_number
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end
        if stats is not UNSET:
            field_dict["stats"] = stats

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        segment_number = d.pop("segment_number", UNSET)

        group_number = d.pop("group_number", UNSET)

        start = d.pop("start", UNSET)

        end = d.pop("end", UNSET)

        stats = d.pop("stats", UNSET)

        plan_stats = cls(
            segment_number=segment_number,
            group_number=group_number,
            start=start,
            end=end,
            stats=stats,
        )

        plan_stats.additional_properties = d
        return plan_stats

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
