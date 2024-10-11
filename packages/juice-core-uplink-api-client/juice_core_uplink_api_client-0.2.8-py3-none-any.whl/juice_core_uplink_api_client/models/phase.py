import datetime
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Phase")


@_attrs_define
class Phase:
    """
    Attributes:
        name (str):
        mnemonic (str):
        start (Union[None, Unset, datetime.datetime]):
        end (Union[None, Unset, datetime.datetime]):
    """

    name: str
    mnemonic: str
    start: None | Unset | datetime.datetime = UNSET
    end: None | Unset | datetime.datetime = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        mnemonic = self.mnemonic

        start: None | Unset | str
        if isinstance(self.start, Unset):
            start = UNSET
        elif isinstance(self.start, datetime.datetime):
            start = self.start.isoformat()
        else:
            start = self.start

        end: None | Unset | str
        if isinstance(self.end, Unset):
            end = UNSET
        elif isinstance(self.end, datetime.datetime):
            end = self.end.isoformat()
        else:
            end = self.end

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mnemonic": mnemonic,
            }
        )
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        def _parse_start(data: object) -> None | Unset | datetime.datetime:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError
                start_type_0 = isoparse(data)

                return start_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | datetime.datetime, data)

        start = _parse_start(d.pop("start", UNSET))

        def _parse_end(data: object) -> None | Unset | datetime.datetime:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError
                end_type_0 = isoparse(data)

                return end_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | datetime.datetime, data)

        end = _parse_end(d.pop("end", UNSET))

        phase = cls(
            name=name,
            mnemonic=mnemonic,
            start=start,
            end=end,
        )

        phase.additional_properties = d
        return phase

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
