from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.phase import Phase


T = TypeVar("T", bound="Trajectory")


@_attrs_define
class Trajectory:
    """
    Attributes:
        name (str):
        mnemonic (str):
        phases (List['Phase']):
        id (Union[Unset, int]):
        pt_context (Union[None, Unset, str]):
        trajectory_type (Union[Unset, str]):
        spice_info (Union[Unset, str]):
        ptr_file (Union[Unset, str]):
    """

    name: str
    mnemonic: str
    phases: list["Phase"]
    id: Unset | int = UNSET
    pt_context: None | Unset | str = UNSET
    trajectory_type: Unset | str = UNSET
    spice_info: Unset | str = UNSET
    ptr_file: Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        mnemonic = self.mnemonic

        phases = []
        for phases_item_data in self.phases:
            phases_item = phases_item_data.to_dict()
            phases.append(phases_item)

        id = self.id

        pt_context: None | Unset | str
        if isinstance(self.pt_context, Unset):
            pt_context = UNSET
        else:
            pt_context = self.pt_context

        trajectory_type = self.trajectory_type

        spice_info = self.spice_info

        ptr_file = self.ptr_file

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mnemonic": mnemonic,
                "phases": phases,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if pt_context is not UNSET:
            field_dict["pt_context"] = pt_context
        if trajectory_type is not UNSET:
            field_dict["trajectory_type"] = trajectory_type
        if spice_info is not UNSET:
            field_dict["spice_info"] = spice_info
        if ptr_file is not UNSET:
            field_dict["ptr_file"] = ptr_file

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.phase import Phase

        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        phases = []
        _phases = d.pop("phases")
        for phases_item_data in _phases:
            phases_item = Phase.from_dict(phases_item_data)

            phases.append(phases_item)

        id = d.pop("id", UNSET)

        def _parse_pt_context(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        pt_context = _parse_pt_context(d.pop("pt_context", UNSET))

        trajectory_type = d.pop("trajectory_type", UNSET)

        spice_info = d.pop("spice_info", UNSET)

        ptr_file = d.pop("ptr_file", UNSET)

        trajectory = cls(
            name=name,
            mnemonic=mnemonic,
            phases=phases,
            id=id,
            pt_context=pt_context,
            trajectory_type=trajectory_type,
            spice_info=spice_info,
            ptr_file=ptr_file,
        )

        trajectory.additional_properties = d
        return trajectory

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
