from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.plan import Plan
from ...types import Response


def _get_kwargs(
    format_: str,
    *,
    body: Plan,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/rest_api/plan_ptr_skeleton{format_}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | None:
    if response.status_code == HTTPStatus.OK:
        return None
    if response.status_code == HTTPStatus.BAD_REQUEST:
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
    format_: str,
    *,
    client: AuthenticatedClient | Client,
    body: Plan,
) -> Response[Any]:
    """Generates a XML PTR file with the pointing information filled

     Adds a new plan to the trajectory

    Args:
        format_ (str):
        body (Plan):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        format_=format_,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    format_: str,
    *,
    client: AuthenticatedClient | Client,
    body: Plan,
) -> Response[Any]:
    """Generates a XML PTR file with the pointing information filled

     Adds a new plan to the trajectory

    Args:
        format_ (str):
        body (Plan):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        format_=format_,
        body=body,
    )

    response = await client.get_async_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)
