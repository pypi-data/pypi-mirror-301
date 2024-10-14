from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.observation_definition import ObservationDefinition
from ...types import Response


def _get_kwargs(
    format_: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/rest_api/observation_definition{format_}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ObservationDefinition | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = ObservationDefinition.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ObservationDefinition]:
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
) -> Response[ObservationDefinition]:
    """Retrieve the observation definition identified by the mnemonic

     Get the list of observation definitions available in the system

    Args:
        format_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ObservationDefinition]
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
) -> ObservationDefinition | None:
    """Retrieve the observation definition identified by the mnemonic

     Get the list of observation definitions available in the system

    Args:
        format_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ObservationDefinition
    """

    return sync_detailed(
        format_=format_,
        client=client,
    ).parsed


async def asyncio_detailed(
    format_: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ObservationDefinition]:
    """Retrieve the observation definition identified by the mnemonic

     Get the list of observation definitions available in the system

    Args:
        format_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ObservationDefinition]
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
) -> ObservationDefinition | None:
    """Retrieve the observation definition identified by the mnemonic

     Get the list of observation definitions available in the system

    Args:
        format_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ObservationDefinition
    """

    return (
        await asyncio_detailed(
            format_=format_,
            client=client,
        )
    ).parsed
