from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.user import User
from ...types import Response


def _get_kwargs(
    username: str,
    format_: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/rest_api/user/{username}{format_}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | User | None:
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == HTTPStatus.OK:
        response_200 = User.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | User]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    username: str,
    format_: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | User]:
    """Retrieve the user details by username

     API endpoint that allows users to be viewed or edited.

    Args:
        username (str):
        format_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, User]]
    """

    kwargs = _get_kwargs(
        username=username,
        format_=format_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    username: str,
    format_: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | User | None:
    """Retrieve the user details by username

     API endpoint that allows users to be viewed or edited.

    Args:
        username (str):
        format_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, User]
    """

    return sync_detailed(
        username=username,
        format_=format_,
        client=client,
    ).parsed


async def asyncio_detailed(
    username: str,
    format_: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | User]:
    """Retrieve the user details by username

     API endpoint that allows users to be viewed or edited.

    Args:
        username (str):
        format_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, User]]
    """

    kwargs = _get_kwargs(
        username=username,
        format_=format_,
    )

    response = await client.get_async_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio(
    username: str,
    format_: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | User | None:
    """Retrieve the user details by username

     API endpoint that allows users to be viewed or edited.

    Args:
        username (str):
        format_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, User]
    """

    return (
        await asyncio_detailed(
            username=username,
            format_=format_,
            client=client,
        )
    ).parsed
