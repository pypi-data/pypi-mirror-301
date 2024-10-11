from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PlnViewSession")


@_attrs_define
class PlnViewSession:
    """
    Attributes:
        ground_station (str):
        activity_start (Union[Unset, str]):
        activity_end (Union[Unset, str]):
        tracking_start (Union[Unset, str]):
        tracking_end (Union[Unset, str]):
        description (Union[Unset, str]):
        origin (Union[Unset, str]):
    """

    ground_station: str
    activity_start: Unset | str = UNSET
    activity_end: Unset | str = UNSET
    tracking_start: Unset | str = UNSET
    tracking_end: Unset | str = UNSET
    description: Unset | str = UNSET
    origin: Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ground_station = self.ground_station

        activity_start = self.activity_start

        activity_end = self.activity_end

        tracking_start = self.tracking_start

        tracking_end = self.tracking_end

        description = self.description

        origin = self.origin

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ground_station": ground_station,
            }
        )
        if activity_start is not UNSET:
            field_dict["activity_start"] = activity_start
        if activity_end is not UNSET:
            field_dict["activity_end"] = activity_end
        if tracking_start is not UNSET:
            field_dict["tracking_start"] = tracking_start
        if tracking_end is not UNSET:
            field_dict["tracking_end"] = tracking_end
        if description is not UNSET:
            field_dict["description"] = description
        if origin is not UNSET:
            field_dict["origin"] = origin

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        ground_station = d.pop("ground_station")

        activity_start = d.pop("activity_start", UNSET)

        activity_end = d.pop("activity_end", UNSET)

        tracking_start = d.pop("tracking_start", UNSET)

        tracking_end = d.pop("tracking_end", UNSET)

        description = d.pop("description", UNSET)

        origin = d.pop("origin", UNSET)

        pln_view_session = cls(
            ground_station=ground_station,
            activity_start=activity_start,
            activity_end=activity_end,
            tracking_start=tracking_start,
            tracking_end=tracking_end,
            description=description,
            origin=origin,
        )

        pln_view_session.additional_properties = d
        return pln_view_session

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
