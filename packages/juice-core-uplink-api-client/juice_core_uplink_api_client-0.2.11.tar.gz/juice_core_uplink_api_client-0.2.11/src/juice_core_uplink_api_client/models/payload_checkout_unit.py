from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PayloadCheckoutUnit")


@_attrs_define
class PayloadCheckoutUnit:
    """
    Attributes:
        name (str):
        mnemonic (str):
        description (Union[None, Unset, str]):
        color (Union[None, Unset, str]):
        instrument (Union[None, Unset, str]):
        sub_instrument (Union[None, Unset, str]):
    """

    name: str
    mnemonic: str
    description: None | Unset | str = UNSET
    color: None | Unset | str = UNSET
    instrument: None | Unset | str = UNSET
    sub_instrument: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        mnemonic = self.mnemonic

        description: None | Unset | str
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        color: None | Unset | str
        if isinstance(self.color, Unset):
            color = UNSET
        else:
            color = self.color

        instrument: None | Unset | str
        if isinstance(self.instrument, Unset):
            instrument = UNSET
        else:
            instrument = self.instrument

        sub_instrument: None | Unset | str
        if isinstance(self.sub_instrument, Unset):
            sub_instrument = UNSET
        else:
            sub_instrument = self.sub_instrument

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mnemonic": mnemonic,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if color is not UNSET:
            field_dict["color"] = color
        if instrument is not UNSET:
            field_dict["instrument"] = instrument
        if sub_instrument is not UNSET:
            field_dict["sub_instrument"] = sub_instrument

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        def _parse_description(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_color(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        color = _parse_color(d.pop("color", UNSET))

        def _parse_instrument(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        instrument = _parse_instrument(d.pop("instrument", UNSET))

        def _parse_sub_instrument(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        sub_instrument = _parse_sub_instrument(d.pop("sub_instrument", UNSET))

        payload_checkout_unit = cls(
            name=name,
            mnemonic=mnemonic,
            description=description,
            color=color,
            instrument=instrument,
            sub_instrument=sub_instrument,
        )

        payload_checkout_unit.additional_properties = d
        return payload_checkout_unit

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
