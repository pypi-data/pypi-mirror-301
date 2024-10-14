from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PlnViewFile")


@_attrs_define
class PlnViewFile:
    """
    Attributes:
        mnemonic (str):
        name (str):
        description (Union[Unset, str]):
    """

    mnemonic: str
    name: str
    description: Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mnemonic = self.mnemonic

        name = self.name

        description = self.description

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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        mnemonic = d.pop("mnemonic")

        name = d.pop("name")

        description = d.pop("description", UNSET)

        pln_view_file = cls(
            mnemonic=mnemonic,
            name=name,
            description=description,
        )

        pln_view_file.additional_properties = d
        return pln_view_file

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
