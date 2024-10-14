from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.working_group_membership_type import WorkingGroupMembershipType
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkingGroupMembership")


@_attrs_define
class WorkingGroupMembership:
    """
    Attributes:
        type (WorkingGroupMembershipType):
        working_group (Union[Unset, str]):
    """

    type: WorkingGroupMembershipType
    working_group: Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type = self.type.value

        working_group = self.working_group

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if working_group is not UNSET:
            field_dict["working_group"] = working_group

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        type = WorkingGroupMembershipType(d.pop("type"))

        working_group = d.pop("working_group", UNSET)

        working_group_membership = cls(
            type=type,
            working_group=working_group,
        )

        working_group_membership.additional_properties = d
        return working_group_membership

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
