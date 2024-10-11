from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PayloadCheckoutWindow")


@_attrs_define
class PayloadCheckoutWindow:
    """
    Attributes:
        name (str):
        mnemonic (str):
        description (Union[None, Unset, str]):
        uevt_file (Union[None, Unset, str]):
        sevt_file (Union[None, Unset, str]):
        git_branch (Union[None, Unset, str]):
        baseline (Union[None, Unset, str]):
        start (Union[None, Unset, str]):
        end (Union[None, Unset, str]):
        ref_event_name (Union[None, Unset, str]):
        ref_event_counter (Union[None, Unset, int]):
    """

    name: str
    mnemonic: str
    description: None | Unset | str = UNSET
    uevt_file: None | Unset | str = UNSET
    sevt_file: None | Unset | str = UNSET
    git_branch: None | Unset | str = UNSET
    baseline: None | Unset | str = UNSET
    start: None | Unset | str = UNSET
    end: None | Unset | str = UNSET
    ref_event_name: None | Unset | str = UNSET
    ref_event_counter: None | Unset | int = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        mnemonic = self.mnemonic

        description: None | Unset | str
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        uevt_file: None | Unset | str
        if isinstance(self.uevt_file, Unset):
            uevt_file = UNSET
        else:
            uevt_file = self.uevt_file

        sevt_file: None | Unset | str
        if isinstance(self.sevt_file, Unset):
            sevt_file = UNSET
        else:
            sevt_file = self.sevt_file

        git_branch: None | Unset | str
        if isinstance(self.git_branch, Unset):
            git_branch = UNSET
        else:
            git_branch = self.git_branch

        baseline: None | Unset | str
        if isinstance(self.baseline, Unset):
            baseline = UNSET
        else:
            baseline = self.baseline

        start: None | Unset | str
        if isinstance(self.start, Unset):
            start = UNSET
        else:
            start = self.start

        end: None | Unset | str
        if isinstance(self.end, Unset):
            end = UNSET
        else:
            end = self.end

        ref_event_name: None | Unset | str
        if isinstance(self.ref_event_name, Unset):
            ref_event_name = UNSET
        else:
            ref_event_name = self.ref_event_name

        ref_event_counter: None | Unset | int
        if isinstance(self.ref_event_counter, Unset):
            ref_event_counter = UNSET
        else:
            ref_event_counter = self.ref_event_counter

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mnemonic": mnemonic,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if uevt_file is not UNSET:
            field_dict["uevt_file"] = uevt_file
        if sevt_file is not UNSET:
            field_dict["sevt_file"] = sevt_file
        if git_branch is not UNSET:
            field_dict["git_branch"] = git_branch
        if baseline is not UNSET:
            field_dict["baseline"] = baseline
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end
        if ref_event_name is not UNSET:
            field_dict["ref_event_name"] = ref_event_name
        if ref_event_counter is not UNSET:
            field_dict["ref_event_counter"] = ref_event_counter

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        def _parse_description(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_uevt_file(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        uevt_file = _parse_uevt_file(d.pop("uevt_file", UNSET))

        def _parse_sevt_file(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        sevt_file = _parse_sevt_file(d.pop("sevt_file", UNSET))

        def _parse_git_branch(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        git_branch = _parse_git_branch(d.pop("git_branch", UNSET))

        def _parse_baseline(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        baseline = _parse_baseline(d.pop("baseline", UNSET))

        def _parse_start(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        start = _parse_start(d.pop("start", UNSET))

        def _parse_end(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        end = _parse_end(d.pop("end", UNSET))

        def _parse_ref_event_name(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        ref_event_name = _parse_ref_event_name(d.pop("ref_event_name", UNSET))

        def _parse_ref_event_counter(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        ref_event_counter = _parse_ref_event_counter(d.pop("ref_event_counter", UNSET))

        payload_checkout_window = cls(
            name=name,
            mnemonic=mnemonic,
            description=description,
            uevt_file=uevt_file,
            sevt_file=sevt_file,
            git_branch=git_branch,
            baseline=baseline,
            start=start,
            end=end,
            ref_event_name=ref_event_name,
            ref_event_counter=ref_event_counter,
        )

        payload_checkout_window.additional_properties = d
        return payload_checkout_window

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
