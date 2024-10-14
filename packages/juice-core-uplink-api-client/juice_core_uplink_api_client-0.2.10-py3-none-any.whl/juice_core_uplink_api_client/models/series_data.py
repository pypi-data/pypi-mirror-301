from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SeriesData")


@_attrs_define
class SeriesData:
    """
    Attributes:
        epoch (Union[None, Unset, str]):
        value (Union[None, Unset, float]):
    """

    epoch: None | Unset | str = UNSET
    value: None | Unset | float = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        epoch: None | Unset | str
        if isinstance(self.epoch, Unset):
            epoch = UNSET
        else:
            epoch = self.epoch

        value: None | Unset | float
        if isinstance(self.value, Unset):
            value = UNSET
        else:
            value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if epoch is not UNSET:
            field_dict["epoch"] = epoch
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_epoch(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        epoch = _parse_epoch(d.pop("epoch", UNSET))

        def _parse_value(data: object) -> None | Unset | float:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | float, data)

        value = _parse_value(d.pop("value", UNSET))

        series_data = cls(
            epoch=epoch,
            value=value,
        )

        series_data.additional_properties = d
        return series_data

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
