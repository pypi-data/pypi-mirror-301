from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs(
    branch: str,
    hexsha: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/rest_api/git/{branch}/{hexsha}/",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | None:
    if response.status_code == HTTPStatus.BAD_REQUEST:
        return None
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        return None
    if response.status_code == HTTPStatus.OK:
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
    branch: str,
    hexsha: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any]:
    """Get the hierarchy contents for Cruise Phase git

     Get the hierarchy contents for Cruise Phase git

    Args:
        branch (str):
        hexsha (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        branch=branch,
        hexsha=hexsha,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    branch: str,
    hexsha: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any]:
    """Get the hierarchy contents for Cruise Phase git

     Get the hierarchy contents for Cruise Phase git

    Args:
        branch (str):
        hexsha (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        branch=branch,
        hexsha=hexsha,
    )

    response = await client.get_async_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)
