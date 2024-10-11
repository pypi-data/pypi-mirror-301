from http import HTTPStatus
from typing import Any, cast

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
        "url": f"/rest_api/plan{format_}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | Plan | None:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = Plan.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | Plan]:
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
) -> Response[Any | Plan]:
    """Adds a new plan

     Adds a new plan to the trajectory

    Args:
        format_ (str):
        body (Plan):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Plan]]
    """

    kwargs = _get_kwargs(
        format_=format_,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    format_: str,
    *,
    client: AuthenticatedClient | Client,
    body: Plan,
) -> Any | Plan | None:
    """Adds a new plan

     Adds a new plan to the trajectory

    Args:
        format_ (str):
        body (Plan):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Plan]
    """

    return sync_detailed(
        format_=format_,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    format_: str,
    *,
    client: AuthenticatedClient | Client,
    body: Plan,
) -> Response[Any | Plan]:
    """Adds a new plan

     Adds a new plan to the trajectory

    Args:
        format_ (str):
        body (Plan):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Plan]]
    """

    kwargs = _get_kwargs(
        format_=format_,
        body=body,
    )

    response = await client.get_async_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio(
    format_: str,
    *,
    client: AuthenticatedClient | Client,
    body: Plan,
) -> Any | Plan | None:
    """Adds a new plan

     Adds a new plan to the trajectory

    Args:
        format_ (str):
        body (Plan):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Plan]
    """

    return (
        await asyncio_detailed(
            format_=format_,
            client=client,
            body=body,
        )
    ).parsed
