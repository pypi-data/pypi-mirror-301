from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResourceProfile")


@_attrs_define
class ResourceProfile:
    """
    Attributes:
        category (str):
        target (str):
        unit (str):
        instrument_type (str):
        value (Union[None, Unset, float]):
    """

    category: str
    target: str
    unit: str
    instrument_type: str
    value: None | Unset | float = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        category = self.category

        target = self.target

        unit = self.unit

        instrument_type = self.instrument_type

        value: None | Unset | float
        if isinstance(self.value, Unset):
            value = UNSET
        else:
            value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "category": category,
                "target": target,
                "unit": unit,
                "instrument_type": instrument_type,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        category = d.pop("category")

        target = d.pop("target")

        unit = d.pop("unit")

        instrument_type = d.pop("instrument_type")

        def _parse_value(data: object) -> None | Unset | float:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | float, data)

        value = _parse_value(d.pop("value", UNSET))

        resource_profile = cls(
            category=category,
            target=target,
            unit=unit,
            instrument_type=instrument_type,
            value=value,
        )

        resource_profile.additional_properties = d
        return resource_profile

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
