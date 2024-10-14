from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Mode")


@_attrs_define
class Mode:
    """
    Attributes:
        name (str):
        mnemonic (str):
        payload (str):
        description (Union[None, Unset, str]):
        mapps_mode (Union[None, Unset, str]):
        power (Union[None, Unset, float]):
        data_rate (Union[None, Unset, float]):
        inactive (Union[Unset, bool]):
        comments (Union[None, Unset, str]):
    """

    name: str
    mnemonic: str
    payload: str
    description: None | Unset | str = UNSET
    mapps_mode: None | Unset | str = UNSET
    power: None | Unset | float = UNSET
    data_rate: None | Unset | float = UNSET
    inactive: Unset | bool = UNSET
    comments: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        mnemonic = self.mnemonic

        payload = self.payload

        description: None | Unset | str
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        mapps_mode: None | Unset | str
        if isinstance(self.mapps_mode, Unset):
            mapps_mode = UNSET
        else:
            mapps_mode = self.mapps_mode

        power: None | Unset | float
        if isinstance(self.power, Unset):
            power = UNSET
        else:
            power = self.power

        data_rate: None | Unset | float
        if isinstance(self.data_rate, Unset):
            data_rate = UNSET
        else:
            data_rate = self.data_rate

        inactive = self.inactive

        comments: None | Unset | str
        if isinstance(self.comments, Unset):
            comments = UNSET
        else:
            comments = self.comments

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mnemonic": mnemonic,
                "payload": payload,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if mapps_mode is not UNSET:
            field_dict["mapps_mode"] = mapps_mode
        if power is not UNSET:
            field_dict["power"] = power
        if data_rate is not UNSET:
            field_dict["data_rate"] = data_rate
        if inactive is not UNSET:
            field_dict["inactive"] = inactive
        if comments is not UNSET:
            field_dict["comments"] = comments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        payload = d.pop("payload")

        def _parse_description(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_mapps_mode(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        mapps_mode = _parse_mapps_mode(d.pop("mapps_mode", UNSET))

        def _parse_power(data: object) -> None | Unset | float:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | float, data)

        power = _parse_power(d.pop("power", UNSET))

        def _parse_data_rate(data: object) -> None | Unset | float:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | float, data)

        data_rate = _parse_data_rate(d.pop("data_rate", UNSET))

        inactive = d.pop("inactive", UNSET)

        def _parse_comments(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        comments = _parse_comments(d.pop("comments", UNSET))

        mode = cls(
            name=name,
            mnemonic=mnemonic,
            payload=payload,
            description=description,
            mapps_mode=mapps_mode,
            power=power,
            data_rate=data_rate,
            inactive=inactive,
            comments=comments,
        )

        mode.additional_properties = d
        return mode

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
