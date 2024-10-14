from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.instrument_resource_profile import InstrumentResourceProfile
    from ..models.resource_profile import ResourceProfile


T = TypeVar("T", bound="Segment")


@_attrs_define
class Segment:
    """
    Attributes:
        start (str):
        end (str):
        segment_definition (str):
        overwritten (bool):
        instrument_overwritten (bool):
        timeline (str):
        name (Union[Unset, str]):
        resources (Union[List['ResourceProfile'], None, Unset]):
        instrument_resources (Union[List['InstrumentResourceProfile'], None, Unset]):
        segment_group (Union[None, Unset, str]):
        platform_power_profile (Union[None, Unset, str]):
        platform_power (Union[None, Unset, float]):
        pointing_request_snippet (Union[None, Unset, str]):
        slew_policy (Union[None, Unset, str]):
        pointing_target (Union[None, Unset, str]):
        scheduling_priority (Union[None, Unset, int]):
        origin (Union[None, Unset, str]):
        prime (Union[None, Unset, str]):
        riders (Union[Unset, List[Union[None, str]]]):
    """

    start: str
    end: str
    segment_definition: str
    overwritten: bool
    instrument_overwritten: bool
    timeline: str
    name: Unset | str = UNSET
    resources: list["ResourceProfile"] | None | Unset = UNSET
    instrument_resources: list["InstrumentResourceProfile"] | None | Unset = UNSET
    segment_group: None | Unset | str = UNSET
    platform_power_profile: None | Unset | str = UNSET
    platform_power: None | Unset | float = UNSET
    pointing_request_snippet: None | Unset | str = UNSET
    slew_policy: None | Unset | str = UNSET
    pointing_target: None | Unset | str = UNSET
    scheduling_priority: None | Unset | int = UNSET
    origin: None | Unset | str = UNSET
    prime: None | Unset | str = UNSET
    riders: Unset | list[None | str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start = self.start

        end = self.end

        segment_definition = self.segment_definition

        overwritten = self.overwritten

        instrument_overwritten = self.instrument_overwritten

        timeline = self.timeline

        name = self.name

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

        segment_group: None | Unset | str
        if isinstance(self.segment_group, Unset):
            segment_group = UNSET
        else:
            segment_group = self.segment_group

        platform_power_profile: None | Unset | str
        if isinstance(self.platform_power_profile, Unset):
            platform_power_profile = UNSET
        else:
            platform_power_profile = self.platform_power_profile

        platform_power: None | Unset | float
        if isinstance(self.platform_power, Unset):
            platform_power = UNSET
        else:
            platform_power = self.platform_power

        pointing_request_snippet: None | Unset | str
        if isinstance(self.pointing_request_snippet, Unset):
            pointing_request_snippet = UNSET
        else:
            pointing_request_snippet = self.pointing_request_snippet

        slew_policy: None | Unset | str
        if isinstance(self.slew_policy, Unset):
            slew_policy = UNSET
        else:
            slew_policy = self.slew_policy

        pointing_target: None | Unset | str
        if isinstance(self.pointing_target, Unset):
            pointing_target = UNSET
        else:
            pointing_target = self.pointing_target

        scheduling_priority: None | Unset | int
        if isinstance(self.scheduling_priority, Unset):
            scheduling_priority = UNSET
        else:
            scheduling_priority = self.scheduling_priority

        origin: None | Unset | str
        if isinstance(self.origin, Unset):
            origin = UNSET
        else:
            origin = self.origin

        prime: None | Unset | str
        if isinstance(self.prime, Unset):
            prime = UNSET
        else:
            prime = self.prime

        riders: Unset | list[None | str] = UNSET
        if not isinstance(self.riders, Unset):
            riders = []
            for riders_item_data in self.riders:
                riders_item: None | str
                riders_item = riders_item_data
                riders.append(riders_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start": start,
                "end": end,
                "segment_definition": segment_definition,
                "overwritten": overwritten,
                "instrument_overwritten": instrument_overwritten,
                "timeline": timeline,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if resources is not UNSET:
            field_dict["resources"] = resources
        if instrument_resources is not UNSET:
            field_dict["instrument_resources"] = instrument_resources
        if segment_group is not UNSET:
            field_dict["segment_group"] = segment_group
        if platform_power_profile is not UNSET:
            field_dict["platform_power_profile"] = platform_power_profile
        if platform_power is not UNSET:
            field_dict["platform_power"] = platform_power
        if pointing_request_snippet is not UNSET:
            field_dict["pointing_request_snippet"] = pointing_request_snippet
        if slew_policy is not UNSET:
            field_dict["slew_policy"] = slew_policy
        if pointing_target is not UNSET:
            field_dict["pointing_target"] = pointing_target
        if scheduling_priority is not UNSET:
            field_dict["scheduling_priority"] = scheduling_priority
        if origin is not UNSET:
            field_dict["origin"] = origin
        if prime is not UNSET:
            field_dict["prime"] = prime
        if riders is not UNSET:
            field_dict["riders"] = riders

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.instrument_resource_profile import InstrumentResourceProfile
        from ..models.resource_profile import ResourceProfile

        d = src_dict.copy()
        start = d.pop("start")

        end = d.pop("end")

        segment_definition = d.pop("segment_definition")

        overwritten = d.pop("overwritten")

        instrument_overwritten = d.pop("instrument_overwritten")

        timeline = d.pop("timeline")

        name = d.pop("name", UNSET)

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

        def _parse_segment_group(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        segment_group = _parse_segment_group(d.pop("segment_group", UNSET))

        def _parse_platform_power_profile(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        platform_power_profile = _parse_platform_power_profile(
            d.pop("platform_power_profile", UNSET)
        )

        def _parse_platform_power(data: object) -> None | Unset | float:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | float, data)

        platform_power = _parse_platform_power(d.pop("platform_power", UNSET))

        def _parse_pointing_request_snippet(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        pointing_request_snippet = _parse_pointing_request_snippet(
            d.pop("pointing_request_snippet", UNSET)
        )

        def _parse_slew_policy(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        slew_policy = _parse_slew_policy(d.pop("slew_policy", UNSET))

        def _parse_pointing_target(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        pointing_target = _parse_pointing_target(d.pop("pointing_target", UNSET))

        def _parse_scheduling_priority(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        scheduling_priority = _parse_scheduling_priority(
            d.pop("scheduling_priority", UNSET)
        )

        def _parse_origin(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        origin = _parse_origin(d.pop("origin", UNSET))

        def _parse_prime(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        prime = _parse_prime(d.pop("prime", UNSET))

        riders = []
        _riders = d.pop("riders", UNSET)
        for riders_item_data in _riders or []:

            def _parse_riders_item(data: object) -> None | str:
                if data is None:
                    return data
                return cast(None | str, data)

            riders_item = _parse_riders_item(riders_item_data)

            riders.append(riders_item)

        segment = cls(
            start=start,
            end=end,
            segment_definition=segment_definition,
            overwritten=overwritten,
            instrument_overwritten=instrument_overwritten,
            timeline=timeline,
            name=name,
            resources=resources,
            instrument_resources=instrument_resources,
            segment_group=segment_group,
            platform_power_profile=platform_power_profile,
            platform_power=platform_power,
            pointing_request_snippet=pointing_request_snippet,
            slew_policy=slew_policy,
            pointing_target=pointing_target,
            scheduling_priority=scheduling_priority,
            origin=origin,
            prime=prime,
            riders=riders,
        )

        segment.additional_properties = d
        return segment

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
