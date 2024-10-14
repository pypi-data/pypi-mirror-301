from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_profile import DataProfile
    from ..models.power_profile import PowerProfile


T = TypeVar("T", bound="ObservationDefinitionExtend")


@_attrs_define
class ObservationDefinitionExtend:
    """
    Attributes:
        name (str):
        mnemonic (str):
        payload (str):
        pointing_type (str):
        target (str):
        segment_definitions (List[str]):
        scheduling_rules (str): any rule that is used to schedule the observation: repetition rules, continuous (plasma
            instruments), one-off, every orbit, every day, etc
        avoidance_rules (str): conditions that make the observation not possible (e.g. thruster firing)
        id (Union[Unset, int]):
        description (Union[None, Unset, str]):
        data_profile (Union[List['DataProfile'], None, Unset]):
        power_profile (Union[List['PowerProfile'], None, Unset]):
        ptr_snippet_file (Union[None, Unset, str]):
        itl_snippet_file (Union[None, Unset, str]):
        ptr_snippet (Union[None, Unset, str]):
        itl_snippet (Union[None, Unset, str]):
        log (Union[None, Unset, str]):
        comments (Union[None, Unset, str]):
        change_reason (Union[None, Unset, str]):
        support_plot_1 (Union[None, Unset, str]):
        support_plot_2 (Union[None, Unset, str]):
        support_plot_3 (Union[None, Unset, str]):
    """

    name: str
    mnemonic: str
    payload: str
    pointing_type: str
    target: str
    segment_definitions: list[str]
    scheduling_rules: str
    avoidance_rules: str
    id: Unset | int = UNSET
    description: None | Unset | str = UNSET
    data_profile: list["DataProfile"] | None | Unset = UNSET
    power_profile: list["PowerProfile"] | None | Unset = UNSET
    ptr_snippet_file: None | Unset | str = UNSET
    itl_snippet_file: None | Unset | str = UNSET
    ptr_snippet: None | Unset | str = UNSET
    itl_snippet: None | Unset | str = UNSET
    log: None | Unset | str = UNSET
    comments: None | Unset | str = UNSET
    change_reason: None | Unset | str = UNSET
    support_plot_1: None | Unset | str = UNSET
    support_plot_2: None | Unset | str = UNSET
    support_plot_3: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        mnemonic = self.mnemonic

        payload = self.payload

        pointing_type = self.pointing_type

        target = self.target

        segment_definitions = self.segment_definitions

        scheduling_rules = self.scheduling_rules

        avoidance_rules = self.avoidance_rules

        id = self.id

        description: None | Unset | str
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        data_profile: list[dict[str, Any]] | None | Unset
        if isinstance(self.data_profile, Unset):
            data_profile = UNSET
        elif isinstance(self.data_profile, list):
            data_profile = []
            for data_profile_type_0_item_data in self.data_profile:
                data_profile_type_0_item = data_profile_type_0_item_data.to_dict()
                data_profile.append(data_profile_type_0_item)

        else:
            data_profile = self.data_profile

        power_profile: list[dict[str, Any]] | None | Unset
        if isinstance(self.power_profile, Unset):
            power_profile = UNSET
        elif isinstance(self.power_profile, list):
            power_profile = []
            for power_profile_type_0_item_data in self.power_profile:
                power_profile_type_0_item = power_profile_type_0_item_data.to_dict()
                power_profile.append(power_profile_type_0_item)

        else:
            power_profile = self.power_profile

        ptr_snippet_file: None | Unset | str
        if isinstance(self.ptr_snippet_file, Unset):
            ptr_snippet_file = UNSET
        else:
            ptr_snippet_file = self.ptr_snippet_file

        itl_snippet_file: None | Unset | str
        if isinstance(self.itl_snippet_file, Unset):
            itl_snippet_file = UNSET
        else:
            itl_snippet_file = self.itl_snippet_file

        ptr_snippet: None | Unset | str
        if isinstance(self.ptr_snippet, Unset):
            ptr_snippet = UNSET
        else:
            ptr_snippet = self.ptr_snippet

        itl_snippet: None | Unset | str
        if isinstance(self.itl_snippet, Unset):
            itl_snippet = UNSET
        else:
            itl_snippet = self.itl_snippet

        log: None | Unset | str
        if isinstance(self.log, Unset):
            log = UNSET
        else:
            log = self.log

        comments: None | Unset | str
        if isinstance(self.comments, Unset):
            comments = UNSET
        else:
            comments = self.comments

        change_reason: None | Unset | str
        if isinstance(self.change_reason, Unset):
            change_reason = UNSET
        else:
            change_reason = self.change_reason

        support_plot_1: None | Unset | str
        if isinstance(self.support_plot_1, Unset):
            support_plot_1 = UNSET
        else:
            support_plot_1 = self.support_plot_1

        support_plot_2: None | Unset | str
        if isinstance(self.support_plot_2, Unset):
            support_plot_2 = UNSET
        else:
            support_plot_2 = self.support_plot_2

        support_plot_3: None | Unset | str
        if isinstance(self.support_plot_3, Unset):
            support_plot_3 = UNSET
        else:
            support_plot_3 = self.support_plot_3

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mnemonic": mnemonic,
                "payload": payload,
                "pointing_type": pointing_type,
                "target": target,
                "segment_definitions": segment_definitions,
                "SchedulingRules": scheduling_rules,
                "AvoidanceRules": avoidance_rules,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if description is not UNSET:
            field_dict["description"] = description
        if data_profile is not UNSET:
            field_dict["data_profile"] = data_profile
        if power_profile is not UNSET:
            field_dict["power_profile"] = power_profile
        if ptr_snippet_file is not UNSET:
            field_dict["PTRSnippet_file"] = ptr_snippet_file
        if itl_snippet_file is not UNSET:
            field_dict["ITLSnippet_file"] = itl_snippet_file
        if ptr_snippet is not UNSET:
            field_dict["PTRSnippet"] = ptr_snippet
        if itl_snippet is not UNSET:
            field_dict["ITLSnippet"] = itl_snippet
        if log is not UNSET:
            field_dict["log"] = log
        if comments is not UNSET:
            field_dict["Comments"] = comments
        if change_reason is not UNSET:
            field_dict["changeReason"] = change_reason
        if support_plot_1 is not UNSET:
            field_dict["Support_Plot_1"] = support_plot_1
        if support_plot_2 is not UNSET:
            field_dict["Support_Plot_2"] = support_plot_2
        if support_plot_3 is not UNSET:
            field_dict["Support_Plot_3"] = support_plot_3

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.data_profile import DataProfile
        from ..models.power_profile import PowerProfile

        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        payload = d.pop("payload")

        pointing_type = d.pop("pointing_type")

        target = d.pop("target")

        segment_definitions = cast(list[str], d.pop("segment_definitions"))

        scheduling_rules = d.pop("SchedulingRules")

        avoidance_rules = d.pop("AvoidanceRules")

        id = d.pop("id", UNSET)

        def _parse_description(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_data_profile(data: object) -> list["DataProfile"] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError
                data_profile_type_0 = []
                _data_profile_type_0 = data
                for data_profile_type_0_item_data in _data_profile_type_0:
                    data_profile_type_0_item = DataProfile.from_dict(
                        data_profile_type_0_item_data
                    )

                    data_profile_type_0.append(data_profile_type_0_item)

                return data_profile_type_0
            except:  # noqa: E722
                pass
            return cast(list["DataProfile"] | None | Unset, data)

        data_profile = _parse_data_profile(d.pop("data_profile", UNSET))

        def _parse_power_profile(data: object) -> list["PowerProfile"] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError
                power_profile_type_0 = []
                _power_profile_type_0 = data
                for power_profile_type_0_item_data in _power_profile_type_0:
                    power_profile_type_0_item = PowerProfile.from_dict(
                        power_profile_type_0_item_data
                    )

                    power_profile_type_0.append(power_profile_type_0_item)

                return power_profile_type_0
            except:  # noqa: E722
                pass
            return cast(list["PowerProfile"] | None | Unset, data)

        power_profile = _parse_power_profile(d.pop("power_profile", UNSET))

        def _parse_ptr_snippet_file(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        ptr_snippet_file = _parse_ptr_snippet_file(d.pop("PTRSnippet_file", UNSET))

        def _parse_itl_snippet_file(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        itl_snippet_file = _parse_itl_snippet_file(d.pop("ITLSnippet_file", UNSET))

        def _parse_ptr_snippet(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        ptr_snippet = _parse_ptr_snippet(d.pop("PTRSnippet", UNSET))

        def _parse_itl_snippet(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        itl_snippet = _parse_itl_snippet(d.pop("ITLSnippet", UNSET))

        def _parse_log(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        log = _parse_log(d.pop("log", UNSET))

        def _parse_comments(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        comments = _parse_comments(d.pop("Comments", UNSET))

        def _parse_change_reason(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        change_reason = _parse_change_reason(d.pop("changeReason", UNSET))

        def _parse_support_plot_1(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        support_plot_1 = _parse_support_plot_1(d.pop("Support_Plot_1", UNSET))

        def _parse_support_plot_2(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        support_plot_2 = _parse_support_plot_2(d.pop("Support_Plot_2", UNSET))

        def _parse_support_plot_3(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        support_plot_3 = _parse_support_plot_3(d.pop("Support_Plot_3", UNSET))

        observation_definition_extend = cls(
            name=name,
            mnemonic=mnemonic,
            payload=payload,
            pointing_type=pointing_type,
            target=target,
            segment_definitions=segment_definitions,
            scheduling_rules=scheduling_rules,
            avoidance_rules=avoidance_rules,
            id=id,
            description=description,
            data_profile=data_profile,
            power_profile=power_profile,
            ptr_snippet_file=ptr_snippet_file,
            itl_snippet_file=itl_snippet_file,
            ptr_snippet=ptr_snippet,
            itl_snippet=itl_snippet,
            log=log,
            comments=comments,
            change_reason=change_reason,
            support_plot_1=support_plot_1,
            support_plot_2=support_plot_2,
            support_plot_3=support_plot_3,
        )

        observation_definition_extend.additional_properties = d
        return observation_definition_extend

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
