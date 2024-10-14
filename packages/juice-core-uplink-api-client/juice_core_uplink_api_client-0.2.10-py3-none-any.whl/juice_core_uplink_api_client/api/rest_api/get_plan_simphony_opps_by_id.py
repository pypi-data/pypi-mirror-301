from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_plan_simphony_opps_by_id_mode import GetPlanSimphonyOppsByIdMode
from ...models.simphony_plan_swagger import SimphonyPlanSwagger
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    start: Unset | str = UNSET,
    end: Unset | str = UNSET,
    mode: Unset | GetPlanSimphonyOppsByIdMode = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["start"] = start

    params["end"] = end

    json_mode: Unset | str = UNSET
    if not isinstance(mode, Unset):
        json_mode = mode.value

    params["mode"] = json_mode

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/rest_api/plan_simphony/opps/{id}/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | SimphonyPlanSwagger | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = SimphonyPlanSwagger.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | SimphonyPlanSwagger]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient | Client,
    start: Unset | str = UNSET,
    end: Unset | str = UNSET,
    mode: Unset | GetPlanSimphonyOppsByIdMode = UNSET,
) -> Response[Any | SimphonyPlanSwagger]:
    r"""Retrieve a plan timeline for Simphony subsystem

     Restricts the returned queries by filtering against a **body** query parameter in the URL.
    The **body** expected value is the JSON string corresponding to the following structure:
    * start: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * end: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * mode: \"strict\" | \"open\" optional: \"open\" Includes the segments partially included in the
    period

    Args:
        id (str):
        start (Union[Unset, str]):
        end (Union[Unset, str]):
        mode (Union[Unset, GetPlanSimphonyOppsByIdMode]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SimphonyPlanSwagger]]
    """

    kwargs = _get_kwargs(
        id=id,
        start=start,
        end=end,
        mode=mode,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient | Client,
    start: Unset | str = UNSET,
    end: Unset | str = UNSET,
    mode: Unset | GetPlanSimphonyOppsByIdMode = UNSET,
) -> Any | SimphonyPlanSwagger | None:
    r"""Retrieve a plan timeline for Simphony subsystem

     Restricts the returned queries by filtering against a **body** query parameter in the URL.
    The **body** expected value is the JSON string corresponding to the following structure:
    * start: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * end: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * mode: \"strict\" | \"open\" optional: \"open\" Includes the segments partially included in the
    period

    Args:
        id (str):
        start (Union[Unset, str]):
        end (Union[Unset, str]):
        mode (Union[Unset, GetPlanSimphonyOppsByIdMode]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SimphonyPlanSwagger]
    """

    return sync_detailed(
        id=id,
        client=client,
        start=start,
        end=end,
        mode=mode,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient | Client,
    start: Unset | str = UNSET,
    end: Unset | str = UNSET,
    mode: Unset | GetPlanSimphonyOppsByIdMode = UNSET,
) -> Response[Any | SimphonyPlanSwagger]:
    r"""Retrieve a plan timeline for Simphony subsystem

     Restricts the returned queries by filtering against a **body** query parameter in the URL.
    The **body** expected value is the JSON string corresponding to the following structure:
    * start: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * end: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * mode: \"strict\" | \"open\" optional: \"open\" Includes the segments partially included in the
    period

    Args:
        id (str):
        start (Union[Unset, str]):
        end (Union[Unset, str]):
        mode (Union[Unset, GetPlanSimphonyOppsByIdMode]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SimphonyPlanSwagger]]
    """

    kwargs = _get_kwargs(
        id=id,
        start=start,
        end=end,
        mode=mode,
    )

    response = await client.get_async_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient | Client,
    start: Unset | str = UNSET,
    end: Unset | str = UNSET,
    mode: Unset | GetPlanSimphonyOppsByIdMode = UNSET,
) -> Any | SimphonyPlanSwagger | None:
    r"""Retrieve a plan timeline for Simphony subsystem

     Restricts the returned queries by filtering against a **body** query parameter in the URL.
    The **body** expected value is the JSON string corresponding to the following structure:
    * start: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * end: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * mode: \"strict\" | \"open\" optional: \"open\" Includes the segments partially included in the
    period

    Args:
        id (str):
        start (Union[Unset, str]):
        end (Union[Unset, str]):
        mode (Union[Unset, GetPlanSimphonyOppsByIdMode]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SimphonyPlanSwagger]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            start=start,
            end=end,
            mode=mode,
        )
    ).parsed
