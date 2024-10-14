from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.detailed_scenario import DetailedScenario
from ...types import Response


def _get_kwargs(
    *,
    body: DetailedScenario,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/rest_api/detailed_scenario/",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | DetailedScenario | None:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = DetailedScenario.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | DetailedScenario]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: DetailedScenario,
) -> Response[Any | DetailedScenario]:
    """Adds a new detailed scenario

     Adds a new plan to the trajectory

    Args:
        body (DetailedScenario):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DetailedScenario]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: DetailedScenario,
) -> Any | DetailedScenario | None:
    """Adds a new detailed scenario

     Adds a new plan to the trajectory

    Args:
        body (DetailedScenario):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DetailedScenario]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: DetailedScenario,
) -> Response[Any | DetailedScenario]:
    """Adds a new detailed scenario

     Adds a new plan to the trajectory

    Args:
        body (DetailedScenario):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DetailedScenario]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: DetailedScenario,
) -> Any | DetailedScenario | None:
    """Adds a new detailed scenario

     Adds a new plan to the trajectory

    Args:
        body (DetailedScenario):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DetailedScenario]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
