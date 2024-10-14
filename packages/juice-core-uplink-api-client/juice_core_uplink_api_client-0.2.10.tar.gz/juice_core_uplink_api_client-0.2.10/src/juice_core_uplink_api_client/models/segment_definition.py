from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.instrument_resource_profile import InstrumentResourceProfile
    from ..models.resource_profile import ResourceProfile


T = TypeVar("T", bound="SegmentDefinition")


@_attrs_define
class SegmentDefinition:
    """
    Attributes:
        name (str):
        mnemonic (str):
        riders (List[str]):
        prime_segment (bool):
        observation_definitions (List[str]):
        description (Union[None, Unset, str]):
        resources (Union[List['ResourceProfile'], None, Unset]):
        instrument_resources (Union[List['InstrumentResourceProfile'], None, Unset]):
        group (Union[Unset, str]):
        pointing_request_file (Union[None, Unset, str]):
        slew_policy (Union[Unset, str]):
        pointing_target (Union[None, Unset, str]):
        platform_power_profile (Union[Unset, str]):
        scheduler_flag (Union[None, Unset, bool]):
        scheduling_priority (Union[None, Unset, int]):
        color (Union[None, Unset, str]):
    """

    name: str
    mnemonic: str
    riders: list[str]
    prime_segment: bool
    observation_definitions: list[str]
    description: None | Unset | str = UNSET
    resources: list["ResourceProfile"] | None | Unset = UNSET
    instrument_resources: list["InstrumentResourceProfile"] | None | Unset = UNSET
    group: Unset | str = UNSET
    pointing_request_file: None | Unset | str = UNSET
    slew_policy: Unset | str = UNSET
    pointing_target: None | Unset | str = UNSET
    platform_power_profile: Unset | str = UNSET
    scheduler_flag: None | Unset | bool = UNSET
    scheduling_priority: None | Unset | int = UNSET
    color: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        mnemonic = self.mnemonic

        riders = self.riders

        prime_segment = self.prime_segment

        observation_definitions = self.observation_definitions

        description: None | Unset | str
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

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

        group = self.group

        pointing_request_file: None | Unset | str
        if isinstance(self.pointing_request_file, Unset):
            pointing_request_file = UNSET
        else:
            pointing_request_file = self.pointing_request_file

        slew_policy = self.slew_policy

        pointing_target: None | Unset | str
        if isinstance(self.pointing_target, Unset):
            pointing_target = UNSET
        else:
            pointing_target = self.pointing_target

        platform_power_profile = self.platform_power_profile

        scheduler_flag: None | Unset | bool
        if isinstance(self.scheduler_flag, Unset):
            scheduler_flag = UNSET
        else:
            scheduler_flag = self.scheduler_flag

        scheduling_priority: None | Unset | int
        if isinstance(self.scheduling_priority, Unset):
            scheduling_priority = UNSET
        else:
            scheduling_priority = self.scheduling_priority

        color: None | Unset | str
        if isinstance(self.color, Unset):
            color = UNSET
        else:
            color = self.color

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mnemonic": mnemonic,
                "riders": riders,
                "prime_segment": prime_segment,
                "observation_definitions": observation_definitions,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if resources is not UNSET:
            field_dict["resources"] = resources
        if instrument_resources is not UNSET:
            field_dict["instrument_resources"] = instrument_resources
        if group is not UNSET:
            field_dict["group"] = group
        if pointing_request_file is not UNSET:
            field_dict["pointing_request_file"] = pointing_request_file
        if slew_policy is not UNSET:
            field_dict["slew_policy"] = slew_policy
        if pointing_target is not UNSET:
            field_dict["pointing_target"] = pointing_target
        if platform_power_profile is not UNSET:
            field_dict["platform_power_profile"] = platform_power_profile
        if scheduler_flag is not UNSET:
            field_dict["scheduler_flag"] = scheduler_flag
        if scheduling_priority is not UNSET:
            field_dict["scheduling_priority"] = scheduling_priority
        if color is not UNSET:
            field_dict["color"] = color

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.instrument_resource_profile import InstrumentResourceProfile
        from ..models.resource_profile import ResourceProfile

        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        riders = cast(list[str], d.pop("riders"))

        prime_segment = d.pop("prime_segment")

        observation_definitions = cast(list[str], d.pop("observation_definitions"))

        def _parse_description(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        description = _parse_description(d.pop("description", UNSET))

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

        group = d.pop("group", UNSET)

        def _parse_pointing_request_file(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        pointing_request_file = _parse_pointing_request_file(
            d.pop("pointing_request_file", UNSET)
        )

        slew_policy = d.pop("slew_policy", UNSET)

        def _parse_pointing_target(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        pointing_target = _parse_pointing_target(d.pop("pointing_target", UNSET))

        platform_power_profile = d.pop("platform_power_profile", UNSET)

        def _parse_scheduler_flag(data: object) -> None | Unset | bool:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | bool, data)

        scheduler_flag = _parse_scheduler_flag(d.pop("scheduler_flag", UNSET))

        def _parse_scheduling_priority(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        scheduling_priority = _parse_scheduling_priority(
            d.pop("scheduling_priority", UNSET)
        )

        def _parse_color(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        color = _parse_color(d.pop("color", UNSET))

        segment_definition = cls(
            name=name,
            mnemonic=mnemonic,
            riders=riders,
            prime_segment=prime_segment,
            observation_definitions=observation_definitions,
            description=description,
            resources=resources,
            instrument_resources=instrument_resources,
            group=group,
            pointing_request_file=pointing_request_file,
            slew_policy=slew_policy,
            pointing_target=pointing_target,
            platform_power_profile=platform_power_profile,
            scheduler_flag=scheduler_flag,
            scheduling_priority=scheduling_priority,
            color=color,
        )

        segment_definition.additional_properties = d
        return segment_definition

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
