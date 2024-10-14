from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    mnemonic: str,
    format_: str,
    *,
    content: Unset | str = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["content"] = content

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/rest_api/trajectory/{mnemonic}/ptr{format_}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | None:
    if response.status_code == HTTPStatus.OK:
        return None
    if response.status_code == HTTPStatus.NOT_FOUND:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    mnemonic: str,
    format_: str,
    *,
    client: AuthenticatedClient | Client,
    content: Unset | str = UNSET,
) -> Response[Any]:
    """Retrieve a trajectory PTR

     Retrieve a PTR corresponding to a trajectory.

    Args:
        mnemonic (str):
        format_ (str):
        content (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        mnemonic=mnemonic,
        format_=format_,
        content=content,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    mnemonic: str,
    format_: str,
    *,
    client: AuthenticatedClient | Client,
    content: Unset | str = UNSET,
) -> Response[Any]:
    """Retrieve a trajectory PTR

     Retrieve a PTR corresponding to a trajectory.

    Args:
        mnemonic (str):
        format_ (str):
        content (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        mnemonic=mnemonic,
        format_=format_,
        content=content,
    )

    response = await client.get_async_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)
