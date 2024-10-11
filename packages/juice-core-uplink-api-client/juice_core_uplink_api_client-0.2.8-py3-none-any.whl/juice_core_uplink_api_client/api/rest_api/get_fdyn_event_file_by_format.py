from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.fdyn_event_file import FdynEventFile
from ...types import Response


def _get_kwargs(
    format_: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/rest_api/fdyn_event_file{format_}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> FdynEventFile | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = FdynEventFile.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[FdynEventFile]:
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
) -> Response[FdynEventFile]:
    """Retrieve the EVTC file active

     Retrieve the EVTC file active

    Args:
        format_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FdynEventFile]
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
) -> FdynEventFile | None:
    """Retrieve the EVTC file active

     Retrieve the EVTC file active

    Args:
        format_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FdynEventFile
    """

    return sync_detailed(
        format_=format_,
        client=client,
    ).parsed


async def asyncio_detailed(
    format_: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[FdynEventFile]:
    """Retrieve the EVTC file active

     Retrieve the EVTC file active

    Args:
        format_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FdynEventFile]
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
) -> FdynEventFile | None:
    """Retrieve the EVTC file active

     Retrieve the EVTC file active

    Args:
        format_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FdynEventFile
    """

    return (
        await asyncio_detailed(
            format_=format_,
            client=client,
        )
    ).parsed
