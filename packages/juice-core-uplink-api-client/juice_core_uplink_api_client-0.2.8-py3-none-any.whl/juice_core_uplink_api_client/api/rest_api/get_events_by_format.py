from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.event import Event
from ...types import Response


def _get_kwargs(
    format_: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/rest_api/events{format_}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | list["Event"] | None:
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Event.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | list["Event"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    format_: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | list["Event"]]:
    """Retrieve the geometry events of a trajectory

     Restricts the returned queries by filtering against a **body** query parameter in the URL.
    The **body** expected value is the JSON string corresponding to the following structure:
    * start: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * end: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * trajectory: the name of the trajectory
    * mnemonics: a list of the names of the events mnemonics

    Args:
        format_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['Event']]]
    """

    kwargs = _get_kwargs(
        format_=format_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    format_: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | list["Event"] | None:
    """Retrieve the geometry events of a trajectory

     Restricts the returned queries by filtering against a **body** query parameter in the URL.
    The **body** expected value is the JSON string corresponding to the following structure:
    * start: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * end: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * trajectory: the name of the trajectory
    * mnemonics: a list of the names of the events mnemonics

    Args:
        format_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['Event']]
    """

    return sync_detailed(
        format_=format_,
        client=client,
    ).parsed


async def asyncio_detailed(
    format_: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | list["Event"]]:
    """Retrieve the geometry events of a trajectory

     Restricts the returned queries by filtering against a **body** query parameter in the URL.
    The **body** expected value is the JSON string corresponding to the following structure:
    * start: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * end: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * trajectory: the name of the trajectory
    * mnemonics: a list of the names of the events mnemonics

    Args:
        format_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['Event']]]
    """

    kwargs = _get_kwargs(
        format_=format_,
    )

    response = await client.get_async_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio(
    format_: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | list["Event"] | None:
    """Retrieve the geometry events of a trajectory

     Restricts the returned queries by filtering against a **body** query parameter in the URL.
    The **body** expected value is the JSON string corresponding to the following structure:
    * start: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * end: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * trajectory: the name of the trajectory
    * mnemonics: a list of the names of the events mnemonics

    Args:
        format_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['Event']]
    """

    return (
        await asyncio_detailed(
            format_=format_,
            client=client,
        )
    ).parsed
