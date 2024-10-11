from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="KernelFile")


@_attrs_define
class KernelFile:
    """
    Attributes:
        name (str):
        mnemonic (str):
        path (str):
    """

    name: str
    mnemonic: str
    path: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        mnemonic = self.mnemonic

        path = self.path

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mnemonic": mnemonic,
                "path": path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        path = d.pop("path")

        kernel_file = cls(
            name=name,
            mnemonic=mnemonic,
            path=path,
        )

        kernel_file.additional_properties = d
        return kernel_file

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
