from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.refresh_json_web_token import RefreshJSONWebToken
from ...types import Response


def _get_kwargs(
    *,
    body: RefreshJSONWebToken,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api-token-refresh/",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> RefreshJSONWebToken | None:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = RefreshJSONWebToken.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[RefreshJSONWebToken]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: RefreshJSONWebToken,
) -> Response[RefreshJSONWebToken]:
    """API View that returns a refreshed token (with new expiration) based on
    existing token

     If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token

    Args:
        body (RefreshJSONWebToken):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RefreshJSONWebToken]
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
    body: RefreshJSONWebToken,
) -> RefreshJSONWebToken | None:
    """API View that returns a refreshed token (with new expiration) based on
    existing token

     If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token

    Args:
        body (RefreshJSONWebToken):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RefreshJSONWebToken
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: RefreshJSONWebToken,
) -> Response[RefreshJSONWebToken]:
    """API View that returns a refreshed token (with new expiration) based on
    existing token

     If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token

    Args:
        body (RefreshJSONWebToken):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RefreshJSONWebToken]
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
    body: RefreshJSONWebToken,
) -> RefreshJSONWebToken | None:
    """API View that returns a refreshed token (with new expiration) based on
    existing token

     If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token

    Args:
        body (RefreshJSONWebToken):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RefreshJSONWebToken
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
