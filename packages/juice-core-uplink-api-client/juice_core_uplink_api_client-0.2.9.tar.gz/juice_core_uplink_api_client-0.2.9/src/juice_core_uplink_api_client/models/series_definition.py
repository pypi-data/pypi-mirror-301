from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SeriesDefinition")


@_attrs_define
class SeriesDefinition:
    """
    Attributes:
        name (str):
        mnemonic (str):
        unit (Union[None, Unset, str]):
        category (Union[Unset, str]):
        description (Union[None, Unset, str]):
    """

    name: str
    mnemonic: str
    unit: None | Unset | str = UNSET
    category: Unset | str = UNSET
    description: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        mnemonic = self.mnemonic

        unit: None | Unset | str
        if isinstance(self.unit, Unset):
            unit = UNSET
        else:
            unit = self.unit

        category = self.category

        description: None | Unset | str
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mnemonic": mnemonic,
            }
        )
        if unit is not UNSET:
            field_dict["unit"] = unit
        if category is not UNSET:
            field_dict["category"] = category
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        def _parse_unit(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        unit = _parse_unit(d.pop("unit", UNSET))

        category = d.pop("category", UNSET)

        def _parse_description(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        description = _parse_description(d.pop("description", UNSET))

        series_definition = cls(
            name=name,
            mnemonic=mnemonic,
            unit=unit,
            category=category,
            description=description,
        )

        series_definition.additional_properties = d
        return series_definition

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
