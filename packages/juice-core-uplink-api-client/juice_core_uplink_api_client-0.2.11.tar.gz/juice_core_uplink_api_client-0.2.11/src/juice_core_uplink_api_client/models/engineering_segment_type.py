from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EngineeringSegmentType")


@_attrs_define
class EngineeringSegmentType:
    """
    Attributes:
        mnemonic (str):
        name (str):
        description (Union[None, Unset, str]):
        power (Union[None, Unset, float]):
    """

    mnemonic: str
    name: str
    description: None | Unset | str = UNSET
    power: None | Unset | float = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mnemonic = self.mnemonic

        name = self.name

        description: None | Unset | str
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        power: None | Unset | float
        if isinstance(self.power, Unset):
            power = UNSET
        else:
            power = self.power

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mnemonic": mnemonic,
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if power is not UNSET:
            field_dict["power"] = power

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        mnemonic = d.pop("mnemonic")

        name = d.pop("name")

        def _parse_description(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_power(data: object) -> None | Unset | float:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | float, data)

        power = _parse_power(d.pop("power", UNSET))

        engineering_segment_type = cls(
            mnemonic=mnemonic,
            name=name,
            description=description,
            power=power,
        )

        engineering_segment_type.additional_properties = d
        return engineering_segment_type

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
