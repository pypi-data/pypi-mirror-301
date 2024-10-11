from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.uvt_event import UvtEvent
from ...types import Response


def _get_kwargs(
    source: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/rest_api/uvt_event/{source}/",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | list["UvtEvent"] | None:
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = UvtEvent.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | list["UvtEvent"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    source: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | list["UvtEvent"]]:
    """Retrieve the geometry events of a trajectory

     Get the event instances

    Args:
        source (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['UvtEvent']]]
    """

    kwargs = _get_kwargs(
        source=source,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    source: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | list["UvtEvent"] | None:
    """Retrieve the geometry events of a trajectory

     Get the event instances

    Args:
        source (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['UvtEvent']]
    """

    return sync_detailed(
        source=source,
        client=client,
    ).parsed


async def asyncio_detailed(
    source: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | list["UvtEvent"]]:
    """Retrieve the geometry events of a trajectory

     Get the event instances

    Args:
        source (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['UvtEvent']]]
    """

    kwargs = _get_kwargs(
        source=source,
    )

    response = await client.get_async_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio(
    source: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | list["UvtEvent"] | None:
    """Retrieve the geometry events of a trajectory

     Get the event instances

    Args:
        source (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['UvtEvent']]
    """

    return (
        await asyncio_detailed(
            source=source,
            client=client,
        )
    ).parsed
