from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.instrument_resource_profile import InstrumentResourceProfile
    from ..models.resource_profile import ResourceProfile


T = TypeVar("T", bound="SegmentGroup")


@_attrs_define
class SegmentGroup:
    """
    Attributes:
        name (str):
        mnemonic (str):
        resources (Union[List['ResourceProfile'], None, Unset]):
        instrument_resources (Union[List['InstrumentResourceProfile'], None, Unset]):
        platform_power_profile (Union[None, Unset, str]):
    """

    name: str
    mnemonic: str
    resources: list["ResourceProfile"] | None | Unset = UNSET
    instrument_resources: list["InstrumentResourceProfile"] | None | Unset = UNSET
    platform_power_profile: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        mnemonic = self.mnemonic

        resources: list[dict[str, Any]] | None | Unset
        if isinstance(self.resources, Unset):
            resources = UNSET
        elif isinstance(self.resources, list):
            resources = []
            for resources_type_0_item_data in self.resources:
                resources_type_0_item = resources_type_0_item_data.to_dict()
                resources.append(resources_type_0_item)

        else:
            resources = self.resources

        instrument_resources: list[dict[str, Any]] | None | Unset
        if isinstance(self.instrument_resources, Unset):
            instrument_resources = UNSET
        elif isinstance(self.instrument_resources, list):
            instrument_resources = []
            for instrument_resources_type_0_item_data in self.instrument_resources:
                instrument_resources_type_0_item = (
                    instrument_resources_type_0_item_data.to_dict()
                )
                instrument_resources.append(instrument_resources_type_0_item)

        else:
            instrument_resources = self.instrument_resources

        platform_power_profile: None | Unset | str
        if isinstance(self.platform_power_profile, Unset):
            platform_power_profile = UNSET
        else:
            platform_power_profile = self.platform_power_profile

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mnemonic": mnemonic,
            }
        )
        if resources is not UNSET:
            field_dict["resources"] = resources
        if instrument_resources is not UNSET:
            field_dict["instrument_resources"] = instrument_resources
        if platform_power_profile is not UNSET:
            field_dict["platform_power_profile"] = platform_power_profile

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.instrument_resource_profile import InstrumentResourceProfile
        from ..models.resource_profile import ResourceProfile

        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        def _parse_resources(data: object) -> list["ResourceProfile"] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError
                resources_type_0 = []
                _resources_type_0 = data
                for resources_type_0_item_data in _resources_type_0:
                    resources_type_0_item = ResourceProfile.from_dict(
                        resources_type_0_item_data
                    )

                    resources_type_0.append(resources_type_0_item)

                return resources_type_0
            except:  # noqa: E722
                pass
            return cast(list["ResourceProfile"] | None | Unset, data)

        resources = _parse_resources(d.pop("resources", UNSET))

        def _parse_instrument_resources(
            data: object,
        ) -> list["InstrumentResourceProfile"] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError
                instrument_resources_type_0 = []
                _instrument_resources_type_0 = data
                for (
                    instrument_resources_type_0_item_data
                ) in _instrument_resources_type_0:
                    instrument_resources_type_0_item = (
                        InstrumentResourceProfile.from_dict(
                            instrument_resources_type_0_item_data
                        )
                    )

                    instrument_resources_type_0.append(instrument_resources_type_0_item)

                return instrument_resources_type_0
            except:  # noqa: E722
                pass
            return cast(list["InstrumentResourceProfile"] | None | Unset, data)

        instrument_resources = _parse_instrument_resources(
            d.pop("instrument_resources", UNSET)
        )

        def _parse_platform_power_profile(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        platform_power_profile = _parse_platform_power_profile(
            d.pop("platform_power_profile", UNSET)
        )

        segment_group = cls(
            name=name,
            mnemonic=mnemonic,
            resources=resources,
            instrument_resources=instrument_resources,
            platform_power_profile=platform_power_profile,
        )

        segment_group.additional_properties = d
        return segment_group

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
