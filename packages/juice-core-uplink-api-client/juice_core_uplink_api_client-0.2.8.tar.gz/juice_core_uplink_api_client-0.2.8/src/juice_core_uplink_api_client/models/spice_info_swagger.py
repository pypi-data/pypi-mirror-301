from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.kernel_file import KernelFile


T = TypeVar("T", bound="SpiceInfoSwagger")


@_attrs_define
class SpiceInfoSwagger:
    """
    Attributes:
        kernels (List['KernelFile']):
        skd_version (str):
        metakernel (str):
    """

    kernels: list["KernelFile"]
    skd_version: str
    metakernel: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kernels = []
        for kernels_item_data in self.kernels:
            kernels_item = kernels_item_data.to_dict()
            kernels.append(kernels_item)

        skd_version = self.skd_version

        metakernel = self.metakernel

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kernels": kernels,
                "skd_version": skd_version,
                "metakernel": metakernel,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.kernel_file import KernelFile

        d = src_dict.copy()
        kernels = []
        _kernels = d.pop("kernels")
        for kernels_item_data in _kernels:
            kernels_item = KernelFile.from_dict(kernels_item_data)

            kernels.append(kernels_item)

        skd_version = d.pop("skd_version")

        metakernel = d.pop("metakernel")

        spice_info_swagger = cls(
            kernels=kernels,
            skd_version=skd_version,
            metakernel=metakernel,
        )

        spice_info_swagger.additional_properties = d
        return spice_info_swagger

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
