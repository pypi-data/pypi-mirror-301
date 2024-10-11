from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.segment import Segment
    from ..models.spice_info_swagger import SpiceInfoSwagger


T = TypeVar("T", bound="SimphonyPlanSwagger")


@_attrs_define
class SimphonyPlanSwagger:
    """
    Attributes:
        trajectory (str):
        mnemonic (str):
        is_public (bool):
        segment_timeline (List['Segment']):
        segment_opportunities (List['Segment']):
        spice_info (List['SpiceInfoSwagger']):
        default_block (str):
        default_slew_policy (str):
        name (Union[Unset, str]):
        description (Union[Unset, str]):
    """

    trajectory: str
    mnemonic: str
    is_public: bool
    segment_timeline: list["Segment"]
    segment_opportunities: list["Segment"]
    spice_info: list["SpiceInfoSwagger"]
    default_block: str
    default_slew_policy: str
    name: Unset | str = UNSET
    description: Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        trajectory = self.trajectory

        mnemonic = self.mnemonic

        is_public = self.is_public

        segment_timeline = []
        for segment_timeline_item_data in self.segment_timeline:
            segment_timeline_item = segment_timeline_item_data.to_dict()
            segment_timeline.append(segment_timeline_item)

        segment_opportunities = []
        for segment_opportunities_item_data in self.segment_opportunities:
            segment_opportunities_item = segment_opportunities_item_data.to_dict()
            segment_opportunities.append(segment_opportunities_item)

        spice_info = []
        for spice_info_item_data in self.spice_info:
            spice_info_item = spice_info_item_data.to_dict()
            spice_info.append(spice_info_item)

        default_block = self.default_block

        default_slew_policy = self.default_slew_policy

        name = self.name

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "trajectory": trajectory,
                "mnemonic": mnemonic,
                "is_public": is_public,
                "segment_timeline": segment_timeline,
                "segment_opportunities": segment_opportunities,
                "spice_info": spice_info,
                "default_block": default_block,
                "default_slew_policy": default_slew_policy,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.segment import Segment
        from ..models.spice_info_swagger import SpiceInfoSwagger

        d = src_dict.copy()
        trajectory = d.pop("trajectory")

        mnemonic = d.pop("mnemonic")

        is_public = d.pop("is_public")

        segment_timeline = []
        _segment_timeline = d.pop("segment_timeline")
        for segment_timeline_item_data in _segment_timeline:
            segment_timeline_item = Segment.from_dict(segment_timeline_item_data)

            segment_timeline.append(segment_timeline_item)

        segment_opportunities = []
        _segment_opportunities = d.pop("segment_opportunities")
        for segment_opportunities_item_data in _segment_opportunities:
            segment_opportunities_item = Segment.from_dict(
                segment_opportunities_item_data
            )

            segment_opportunities.append(segment_opportunities_item)

        spice_info = []
        _spice_info = d.pop("spice_info")
        for spice_info_item_data in _spice_info:
            spice_info_item = SpiceInfoSwagger.from_dict(spice_info_item_data)

            spice_info.append(spice_info_item)

        default_block = d.pop("default_block")

        default_slew_policy = d.pop("default_slew_policy")

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        simphony_plan_swagger = cls(
            trajectory=trajectory,
            mnemonic=mnemonic,
            is_public=is_public,
            segment_timeline=segment_timeline,
            segment_opportunities=segment_opportunities,
            spice_info=spice_info,
            default_block=default_block,
            default_slew_policy=default_slew_policy,
            name=name,
            description=description,
        )

        simphony_plan_swagger.additional_properties = d
        return simphony_plan_swagger

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
